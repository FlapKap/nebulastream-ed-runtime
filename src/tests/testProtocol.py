from unittest import unittest
import protocol
from expression import CONST, MUL, LT, GT, Expression
from datatypes import INT8, INT16, INT32
from operators import *


class TestProtocol(unittest.TestCase):

    def test_empty_msg(self):
        raw_msg = b''
        msg = protocol.decode_input_msg(raw_msg)

        expected = []
        self.assertEqual(msg, expected)

    def test_map_msg(self):
        raw_msg = b'\n\x11\n\x01\x04\x12\x0c\n\n\n\x06\n\x04\x00\x04\x08\n\x10\x01'
        op = protocol.decode_input_msg(raw_msg)
        expected = [
            Query([Map(Expression(bytes([CONST, INT32, 8, MUL])), 1)], [INT32])]
        self.assertEqual(op, expected)
        # self.assertEqual(op.operations[0], expected.operations[0])
        # self.assertEqual(op.resultType, expected.resultType)

    def test_filter_msg(self):
        raw_msg = b'\n\x0c\x12\n\x12\x08\n\x06\n\x04\x00\x00\x08\x05'
        op = protocol.decode_input_msg(raw_msg)

        expected = [
            Query([Filter(Expression(bytes([CONST, INT8, 8, LT])))], None)]
        self.assertEqual(op, expected)

    def test_map_filter_msg(self):
        raw_msg = b'\n\x1b\n\x01\x04\x12\n\n\x08\n\x06\n\x04\x00\x04\x08\n\x12\n\x12\x08\n\x06\n\x04\x00\x022\x06'
        ops = protocol.decode_input_msg(raw_msg)

        expected = [Query([
            Map(Expression(bytes([CONST, INT32, 8, MUL])), 0),
            Filter(Expression(bytes([CONST, INT16, 50, GT])))
        ], [INT32])]

        self.assertEqual(ops, expected)

    def test_window_msg(self):
        raw_msg = b'\n\x13\n\x01\x04\x12\x0e\x1a\x0c\x08\x03\x10\x01\x18\x04(\x010\x028\x03'
        op = protocol.decode_input_msg(raw_msg)
        expected = [
            Query(
                [TumblingWindow(WindowSizeType.COUNTBASED, WindowAggregationType.COUNT, 3, 0, 1, 2, 3)], [INT32])]

        self.assertEqual(op, expected)

    def test_multiple_queries(self):
        raw_msg = b'\n\x0e\n\x01\x00\x12\t\n\x07\n\x05\n\x03\x00\x00\x01\n\x1f\n\x01\x04\x12\x0e\x1a\x0c\x08\x03\x10\x01\x18\x04(\x010\x028\x03\x12\n\x12\x08\n\x06\n\x04\x00\x00\x08\x05'
        expected = [
            Query([Map(Expression(bytes([CONST, INT8, 1])), 0)], [INT8]),
            Query([
                TumblingWindow(WindowSizeType.COUNTBASED,
                               WindowAggregationType.COUNT, 3, 0, 1, 2, 3),
                Filter(Expression(bytes([CONST, INT8, 8, LT])))
            ], [INT32]
            )
        ]
        op = protocol.decode_input_msg(raw_msg)
        self.assertEqual(op, expected)

    def test_output_single_response(self):
        raw_msg = b'\n!\x08\x01\x12\x05HELLO\x12\x05THERE\x12\x07GENERAL\x12\x06KENOBI'
        msg = protocol.encode_output_msg(
            {'responses': [{'id': 1, 'response': [b'HELLO', b'THERE', b'GENERAL', b'KENOBI']}]})
        self.assertEqual(msg, raw_msg)

    def test_output_multiple_responses(self):
        raw_msg = b'\n\x05\x08\x01\x12\x01I\n\x08\x08\x02\x12\x04KNOW\n\x07\x08\x03\x12\x03HIM\n\x07\x08\x04\x12\x03HES\n\x06\x08\x05\x12\x02ME'
        msg = protocol.encode_output_msg({'responses': [
            {'id': 1, 'response': [b'I']},
            {'id': 2, 'response': [b'KNOW']},
            {'id': 3, 'response': [b'HIM']},
            {'id': 4, 'response': [b'HES']},
            {'id': 5, 'response': [b'ME']},
        ]})
        self.assertEqual(msg, raw_msg)
