from EndDeviceProtocol import *
from EndDeviceProtocol import ExpressionInstructions as Einstr

# This file is used to generate the binary protobuf messages that are used for testing
# the protocol implementation in ../src/protocol.py

if __name__ == "__main__":
    # generate messages
    empty_msg = Message(queries=[])

    map_msg = Message(queries=[
        Query(operations=[Operation(MapOperation(
            [
                Data(Einstr.CONST),
                Data(_uint8=8),
                Data(Einstr.MUL)
            ],
            attribute=1))])
    ])

    filter_msg = Message(queries=[Query([Operation(filter=FilterOperation(
        predicate=[Data(Einstr.CONST),
                              Data(_uint8=8),
                              Data(Einstr.LT)]
                             ))])])

    map_filter_msg = Message(queries=[Query([
        Operation(map=MapOperation(
            [Data(Einstr.CONST),
                        Data(_uint8=8), Data(Einstr.MUL)])),
        Operation(filter=FilterOperation(predicate=[Data(Einstr.CONST), Data(_int8=50), Data(Einstr.GT)]))])])

    window_msg = Message(queries=[Query([
        Operation(window=WindowOperation(3, WindowSizeType.COUNTBASED, WindowAggregationType.COUNT, 0, 1, 2, 3))])])

    multiple_msg = Message(
        queries=[
            Query(
                operations=[Operation(
                    map=MapOperation(
                        function=[Data(Einstr.CONST),
                                             Data(_uint8=8)], attribute=0))
                            ]
            ),
            Query([
                Operation(window=WindowOperation(
                    3, WindowSizeType.COUNTBASED, WindowAggregationType.COUNT, 0, 1, 2, 3)),
                Operation(filter=FilterOperation(
                    predicate=[Data(Einstr.CONST), Data(_int8=50), Data(Einstr.LT)]))])
        ]
    )

    output_single_msg = Output([OutputQueryResponse(
        1, [Data(_uint8=ord('H')), Data(_uint8=ord('E')), Data(_uint8=ord('L')), Data(_uint8=ord('L')), Data(_uint8=ord('O'))])])

    output_multiple_msg = Output([
        OutputQueryResponse(1, [Data(_uint8=ord('H'))]),
        OutputQueryResponse(2, [Data(_uint8=ord('E'))]),
        OutputQueryResponse(3, [Data(_uint8=ord('L'))]),
        OutputQueryResponse(4, [Data(_uint8=ord('L'))]),
        OutputQueryResponse(5, [Data(_uint8=ord('O'))]),
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
    print("multiple_msg")
    print(multiple_msg.SerializeToString())
    print(multiple_msg.to_dict())
    print()
    print("output_msg_single")
    print(output_single_msg.SerializeToString())
    print(output_single_msg.to_dict())
    print()
    print("output_msg_multiple")
    print(output_multiple_msg.SerializeToString())
    print(output_multiple_msg.to_dict())
