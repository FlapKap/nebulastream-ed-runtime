import minipb
import logging
import operators
# schema
# should correspond to schema found in ../proto/protocol.proto
# these are placed here instead of in the operation objects, since they all use the expression schema

output_entry_schema = (("key", "t"), ("value", "a"),)
output_schema = (("values", "+[", output_entry_schema, "]"),)

expression_schema = (('instructions','a'),)

filter_schema = (("predicate", expression_schema),)
map_schema = (("function", expression_schema),)

operation_types = (
    ("map", map_schema),
    ("filter", filter_schema),
)
message_schema = (
    ("operations", "+[", operation_types, "]")
)

__wire_input = minipb.Wire(message_schema, loglevel=logging.getLogger(__name__).getEffectiveLevel())
__wire_output = minipb.Wire(output_schema)

def has_msg(name, msg):
    return name in msg.keys() and msg[name] is not None

def decode_bytes(b):
    msg= __wire_input.decode(b)
    if has_msg("map", msg):
        return operators.Map(**msg["map"])
    if has_msg("filter", msg):
        return operators.Filter(**msg["filter"])
    return None


## notes - taken from https://github.com/dogtopus/minipb/wiki/Schema-Representations
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
