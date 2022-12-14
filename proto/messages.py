# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: EndDeviceProtocol.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


class ExpressionTypes(betterproto.Enum):
    """
    region expression enumstypes and instructions are taken from
    expression.pythese are not used generally, but are here for reference
    """

    INT8 = 0
    UINT8 = 1
    INT16 = 2
    UINT16 = 3
    INT32 = 4
    UINT32 = 5
    INT64 = 6
    UINT64 = 7
    FLOAT = 8
    DOUBLE = 9


class ExpressionInstructions(betterproto.Enum):
    CONST = 0
    VAR = 1
    AND = 2
    OR = 3
    NOT = 4
    LT = 5
    GT = 6
    EQ = 7
    ADD = 8
    SUB = 9
    MUL = 10
    DIV = 11
    MOD = 12


class WindowAggregationType(betterproto.Enum):
    MIN = 0
    MAX = 1
    SUM = 2
    AVG = 3
    COUNT = 4


class WindowSizeType(betterproto.Enum):
    TIMEBASED = 0
    COUNTBASED = 1


@dataclass
class Output(betterproto.Message):
    values: List["OutputEntry"] = betterproto.message_field(1)


@dataclass
class OutputEntry(betterproto.Message):
    key: int = betterproto.int32_field(1)
    value: bytes = betterproto.bytes_field(2)


@dataclass
class Expression(betterproto.Message):
    instructions: bytes = betterproto.bytes_field(1)


@dataclass
class MapOperation(betterproto.Message):
    function: "Expression" = betterproto.message_field(1)


@dataclass
class FilterOperation(betterproto.Message):
    predicate: "Expression" = betterproto.message_field(1)


@dataclass
class WindowOperation(betterproto.Message):
    size: int = betterproto.int32_field(1)
    size_type: "WindowSizeType" = betterproto.enum_field(2)
    agg_type: "WindowAggregationType" = betterproto.enum_field(3)


@dataclass
class Message(betterproto.Message):
    operations: List["MessageOperation"] = betterproto.message_field(1)


@dataclass
class MessageOperation(betterproto.Message):
    map: "MapOperation" = betterproto.message_field(1)
    filter: "FilterOperation" = betterproto.message_field(2)
    window: "WindowOperation" = betterproto.message_field(3)
