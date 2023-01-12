import minipb
import logging
import operators
from expression import Expression
# schema
# should correspond to schema found in ../proto/protocol.proto
# these are placed here instead of in the operation objects, since they all use the expression schema

__output_entry_schema = (("value", "a"),)
__output_schema = (("values", "+[", __output_entry_schema, "]"),)

__expression_schema = (('instructions', 'a'),)

__filter_schema = (("predicate", __expression_schema),)
__map_schema = (("function", __expression_schema),)
__window_schema = (
    ("size", "t"),
    ("sizeType", "t"),
    ("aggregationType", "t"),
    ("startAttribute", "t"),
    ("endAttribute", "t"),
    ("resultAttribute", "t"),
    ("readAttribute", "t"),)


# This is supposed to be a oneof, but the minipb doesnt seem to be able to enforce that
__operation_types = (
    ("map", __map_schema),
    ("filter", __filter_schema),
    ("window", __window_schema),
)
__message_schema = (
    ("operations", "+[", __operation_types, "]"),
)

__wire_input = minipb.Wire(
    __message_schema, loglevel=logging.getLogger(__name__).getEffectiveLevel())
__wire_output = minipb.Wire(__output_schema)


def has_msg(name, msg):
    return isinstance(msg, dict) and name in msg.keys() and msg[name] is not None


def decode_input_msg(b) -> list[operators.Operator]:
    operations = __wire_input.decode(b)["operations"]
    res = []
    for op in operations:
        if has_msg("map", op):
            opmap = op['map']
            if 'attribute' not in opmap.keys() or opmap['attribute'] is None:
                opmap['attribute'] = 0

            res.append(operators.Map(Expression(
                opmap['function']['instructions']), opmap['attribute']))

        if has_msg("filter", op):
            res.append(operators.Filter(Expression(op['filter']['predicate']['instructions'])))
        
        if has_msg("window", op):
            opwindow = op['window']
            for k, v in opwindow.items():
                if k in ("startAttribute", "endAttribute", "resultAttribute", "readAttribute") and v is None:
                    opwindow[k] = 0
            res.append(operators.TumblingWindow(**opwindow))
    return res


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
