import minipb
import logging
import operators
from expression import Expression
import datatypes
# schema
# should correspond to schema found in ../proto/protocol.proto
# these are placed here instead of in the operation objects, since they all use the expression schema

__output_query_response_schema = (('id', 't'), ('response', '+a'),)
__output_queryresponses_schema = (
    ('responses', '+[', __output_query_response_schema, ']'),)

__value_schema = (
    ('value', (
        ('_uint8_32', 'T'),
        ('_uint64', 'T'),
        ('_int8_32', 'z'),
        ('_int64', 'z'),
        ('_float', 'f'),
        ('_double', 'd'),
    ),
    ),
)

__data_schema = (
    ('data', (
        # An Enum is in protobuf represented as 32bit vint. Therefore 'a' here
        # https://github.com/dogtopus/minipb/wiki/High-level-Protobuf-Features#enums
        ('instruction', 'a'),
        ('value', __value_schema),
    )
    ),
)

__expression_schema = (('instructions', '+[', __data_schema, ']',),)

__filter_schema = (('predicate', __expression_schema,),)
__map_schema = (('function', __expression_schema), ('attribute', 't'),)
__window_schema = (
    ('size', 't'),
    ('sizeType', 't'),
    ('aggregationType', 't'),
    ('startAttribute', 't'),
    ('endAttribute', 't'),
    ('resultAttribute', 't'),
    ('readAttribute', 't'),
)


# This is supposed to be a oneof, but the minipb doesnt seem to be able to enforce that
__operation_types = (
    ('map', __map_schema),
    ('filter', __filter_schema),
    ('window', __window_schema),
)

__query_schema = (
    ('resultType', 'a'),
    ('operations', '+[', __operation_types, ']'),
)

__message_schema = (
    ('queries', '+[', __query_schema, ']'),
)

__wire_input = minipb.Wire(
    __message_schema, loglevel=logging.getLogger(__name__).getEffectiveLevel())
__wire_output = minipb.Wire(__output_queryresponses_schema)


def has_msg(name, msg) -> bool:
    return isinstance(msg, dict) and name in msg.keys() and msg[name] is not None


def decode_input_msg(b) -> list[operators.Query]:
    queries_raw = __wire_input.decode(b)["queries"]
    queries = []
    for operations_raw in queries_raw:
        operations = []
        resultType = datatypes.unpack_array_fixed_type(
            datatypes.INT8, operations_raw["resultType"]) if operations_raw["resultType"] is not None else None
        for op_raw in operations_raw["operations"]:
            if has_msg("map", op_raw):
                opmap = op_raw['map']
                if 'attribute' not in opmap.keys() or opmap['attribute'] is None:
                    opmap['attribute'] = 0

                operations.append(operators.Map(Expression(
                    opmap['function']['instructions']), opmap['attribute']))

            if has_msg("filter", op_raw):
                operations.append(operators.Filter(Expression(
                    op_raw['filter']['predicate']['instructions'])))

            if has_msg("window", op_raw):
                opwindow = op_raw['window']
                for k, v in opwindow.items():
                    if k in ("startAttribute", "endAttribute", "resultAttribute", "readAttribute") and v is None:
                        opwindow[k] = 0
                operations.append(operators.TumblingWindow(**opwindow))
        queries.append(operators.Query(operations, resultType))

    return queries


def encode_output_msg(msg) -> bytes:
    """_summary_
    Args:
        msg (Dict): dict must have key "values" with an array of dicts with
         "value" where  value is bytes.
         Example: `{"values": [{"value": b'1'}, {"value", b'a'}]}`

    Returns:
        bytes: the encoded message
    """
    return __wire_output.encode(msg)


# notes - taken from https://github.com/dogtopus/minipb/wiki/Schema-Representations
# Table of data types
# | Type | Protobuf type  | Python type | Comments                                        |
# |------|----------------|-------------|-------------------------------------------------|
# | `i`  | sfixed32       | int         | 32-bit signed integer, little endian            |
# | `I`  | fixed32        | int         | 32-bit unsigned integer, little endian          |
# | `q`  | sfixed64       | int         | 64-bit signed integer, little endian            |
# | `Q`  | fixed64        | int         | 64-bit unsigned integer, little endian          |
# | `l`  | sfixed32       | int         | Alias of `i`                                    |
# | `L`  | sfixed32       | int         | Alias of `I`                                    |
# | `f`  | float          | float       | 32-bit float                                    |
# | `d`  | double         | float       | 64-bit float                                    |
# | `a`  | bytes          | bytes       |                                                 |
# | `b`  | bool           | bool        |                                                 |
# | `z`  | sint32, sint64 | int         | Signed vint encoded with zigzag (2)             |
# | `t`  | int32, int64   | int         | Signed vint encoded with two's complement (1)   |
# | `T`  | uint32, uint64 | int         | Unsigned vint encoded with two's complement (2) |
# | `U`  | string         | str         | UTF-8 encoding is assumed                       |
# | `v`  | sint32, sint64 | int         | Alias of `z`                                    |
# | `V`  | uint32, uint64 | int         | Alias of `T`                                    |
# | `x`  | empty field    |             |                                                 |

# prefixes
# | Prefix | Protobuf equivalent          | Comments |
# |--------|------------------------------|----------|
# | `*`    | `required ...`               | (1)      |
# | `+`    | `repeated ...`               | (2)      |
# | `#`    | `repeated ... [packed=true]` | (3)      |
# | `[`    | `message  { ... };  ...`     | (4)      |
