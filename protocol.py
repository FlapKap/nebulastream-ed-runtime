import minipb

# schema
# should correspond to
# message output_entry_schema {
#   int key = 1;
#   bytes value = 2;
# }
# message output_entry {
#   repeated output_entry_schema = 1;
# }

output_entry_schema = (("key", "t"), ("value", "a"),)
output_schema = (("values", "+[", output_entry_schema, "]"),)

expression_schema = (("instructions", "+z"))

filter_schema = (("predicate", expression_schema))
map_schema = (("function", expression_schema))

message_types = ((
    ("map", map_schema),
    ("filter", filter_schema)
))
message_schema = (("message", message_types))

__wire_input = minipb.Wire(message_schema)
__wire_output = minipb.Wire(output_schema)

def decodeBytes(b: bytes):
    msg: dict = __wire_input.decode(b)
    for m in msg["message"]:
        if m is not None:
            return m
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
