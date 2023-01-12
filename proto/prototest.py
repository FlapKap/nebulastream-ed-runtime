from messages import *
from messages import ExpressionInstructions as Einstr
from messages import ExpressionTypes as Etype

# This file is used to generate the binary protobuf messages that are used for testing
# the protocol implementation in ../src/protocol.py

if __name__ == "__main__":
    # generate messages
    empty_msg = Message(queries=[])

    map_msg = Message(queries=[
        Query(operations=[QueryOperation(map=MapOperation(
            Expression(instructions=bytes([Einstr.CONST, Etype.INT32, 8, Einstr.MUL])), attribute=0))])
    ])

    filter_msg = Message(queries=[Query(operations=[QueryOperation(filter=FilterOperation(
        predicate=Expression(instructions=bytes([Einstr.CONST, Etype.INT8, 8, Einstr.LT]))))])])

    map_filter_msg = Message(queries=[Query(operations=[QueryOperation(map=MapOperation(
        Expression(instructions=bytes([Einstr.CONST, Etype.INT32, 8, Einstr.MUL])))),
        QueryOperation(filter=FilterOperation(predicate=Expression(instructions=bytes([Einstr.CONST, Etype.INT16, 50, Einstr.GT]))))])])

    window_msg = Message(queries=[Query(operations=[
        QueryOperation(window=WindowOperation(3, WindowSizeType.COUNTBASED, WindowAggregationType.COUNT, 0, 1, 2, 3))])])

    output_single_msg = Output([OutputQueryResponse([b'HELLO',b'THERE',b'GENERAL',b'KENOBI'])])
    
    output_multiple_msg = Output([
        OutputQueryResponse([b'I']),
        OutputQueryResponse([b'KNOW']),
        OutputQueryResponse([b'HIM']),
        OutputQueryResponse([b'HES']),
        OutputQueryResponse([b'ME']),
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
    print()
    print("output_msg_single")
    print(output_single_msg.SerializeToString())
    print(output_single_msg.to_dict())
    print()
    print("output_msg_multiple")
    print(output_multiple_msg.SerializeToString())
    print(output_multiple_msg.to_dict())


