import struct
from micropython import const

INT8 = const(0)
UINT8 = const(1)
INT16 = const(2)
UINT16 = const(3)
INT32 = const(4)
UINT32 = const(5)
INT64 = const(6)
UINT64 = const(7)
FLOAT = const(8)
DOUBLE = const(9)

type_to_fmt = {
    INT8: "<b",
    UINT8: "<B",
    INT16: "<h",
    UINT16: "<H",
    INT32: "<i",
    UINT32: "<I",
    INT64: "<q",
    UINT64: "<Q",
    FLOAT: "<f",
    DOUBLE: "<d"
}

type_to_name = {
    INT8: "INT8",
    UINT8: "UINT8",
    INT16: "INT16",
    UINT16: "UINT16",
    INT32: "INT32",
    UINT32: "UINT32",
    INT64: "INT64",
    UINT64: "UINT64",
    FLOAT: "FLOAT",
    DOUBLE: "DOUBLE"
}


def pack_type(value_type, value) -> bytes:
    return struct.pack(type_to_fmt[value_type], value)

def unpack_array_fixed_type(typ, array):
    return list(array)

def pack_array(types, values) -> bytes:
    res = b''
    for typ, val in zip(types, values):
        res += (pack_type(typ, val))

    return res
