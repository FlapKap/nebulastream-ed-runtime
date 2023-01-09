from messages import *
from messages import ExpressionInstructions as Einstr
from messages import ExpressionTypes as Etype

# This file is used to generate the binary protobuf messages that are used for testing
# the protocol implementation in ../src/protocol.py

if __name__ == "__main__":
    # generate messages
    empty_msg = Message(operations=[])

    map_msg = Message(operations=[MessageOperation(map=MapOperation(
        Expression(instructions=bytes([Einstr.CONST, Etype.INT32, 8, Einstr.MUL]))))])

    filter_msg = Message(operations=[MessageOperation(filter=FilterOperation(
        predicate=Expression(instructions=bytes([Einstr.CONST, Etype.INT8, 8, Einstr.LT]))))])

    map_filter_msg = Message(operations=[MessageOperation(map=MapOperation(
        Expression(instructions=bytes([Einstr.CONST, Etype.INT32, 8, Einstr.MUL])))),
        MessageOperation(filter=FilterOperation(predicate=Expression(instructions=bytes([Einstr.CONST, Etype.INT16, 50, Einstr.GT]))))])

    window_msg = Message(operations=[
        MessageOperation(window=WindowOperation(3,WindowSizeType.COUNTBASED,agg_type=WindowAggregationType.COUNT))
    ])
    print("empty_msg")
    print(empty_msg.SerializeToString())
    print(empty_msg.to_dict())
    print()
    print("map_msg")
    print(map_msg.SerializeToString())
    print(map_msg.to_dict())
    print("filter_msg")
    print(filter_msg.SerializeToString())
    print(filter_msg.to_dict())
    print()
    print("map_filter_msg")
    print(map_filter_msg.SerializeToString())
    print(map_filter_msg.to_dict())
    print()
    print("window_msg")
    print(window_msg.SerializeToString())
    print(window_msg.to_dict())