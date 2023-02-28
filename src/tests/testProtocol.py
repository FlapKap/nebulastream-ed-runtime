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
        raw_msg = b'\n\x12\n\x10\n\x0e\n\x02\x08\x00\n\x02\x10\x08\n\x02\x08\n\x10\x01'

        op = protocol.decode_input_msg(raw_msg)
        expected = [
            Query([Map(Expression([CONST, 8, MUL]), 1)])]
        self.assertEqual(op, expected)

        # self.assertEqual(op.operations[0], expected.operations[0])
        # self.assertEqual(op.resultType, expected.resultType)

    def test_filter_msg(self):
        raw_msg = b'\n\x10\n\x0e\x12\x0c\n\x02\x08\x00\n\x02\x10\x08\n\x02\x08\x05'
        op = protocol.decode_input_msg(raw_msg)

        expected = [
            Query([Filter(Expression([CONST, 8, LT]))])]
        self.assertEqual(op, expected)

    def test_map_filter_msg(self):
        raw_msg = b'\n \n\x0e\n\x0c\n\x02\x08\x00\n\x02\x10\x08\n\x02\x08\n\n\x0e\x12\x0c\n\x02\x08\x00\n\x020d\n\x02\x08\x06'
        ops = protocol.decode_input_msg(raw_msg)

        expected = [Query([
            Map(Expression([CONST, 8, MUL]), 0),
            Filter(Expression([CONST, 50, GT]))
        ])]

        self.assertEqual(ops, expected)

    def test_window_msg(self):
        raw_msg = b'\n\x10\n\x0e\x1a\x0c\x08\x03\x10\x01\x18\x04(\x010\x028\x03'
        op = protocol.decode_input_msg(raw_msg)
        expected = [
            Query(
                [TumblingWindow(WindowSizeType.COUNTBASED, WindowAggregationType.COUNT, 3, 0, 1, 2, 3)])]

        self.assertEqual(op, expected)

    def test_multiple_queries(self):
        raw_msg = b'\n\x0c\n\n\n\x08\n\x02\x08\x00\n\x02\x10\x08\n \n\x0e\x1a\x0c\x08\x03\x10\x01\x18\x04(\x010\x028\x03\n\x0e\x12\x0c\n\x02\x08\x00\n\x020d\n\x02\x08\x05'
        expected = [
            Query([Map(Expression([CONST, 8]), 0)]),
            Query([
                TumblingWindow(WindowSizeType.COUNTBASED,
                               WindowAggregationType.COUNT, 3, 0, 1, 2, 3),
                Filter(Expression([CONST, 50, LT]))
            ]
            )
        ]
        op = protocol.decode_input_msg(raw_msg)
        self.assertEqual(op, expected)

    def test_output_single_response(self):
        raw_msg = b'\n\x16\x08\x01\x12\x02\x10H\x12\x02\x10E\x12\x02\x10L\x12\x02\x10L\x12\x02\x10O'
        msg = protocol.encode_output_msg(
            {'responses': [
                {'id': 1, 'response': [
                    {'_uint8': ord('H'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None},
                    {'_uint8': ord('E'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None},
                    {'_uint8': ord('L'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None},
                    {'_uint8': ord('L'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None},
                    {'_uint8': ord('O'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}
                ]
                }
            ]
            }
        )
        self.assertEqual(msg, raw_msg)

    def test_output_multiple_responses(self):
        raw_msg = b'\n\x06\x08\x01\x12\x02\x10H\n\x06\x08\x02\x12\x02\x10E\n\x06\x08\x03\x12\x02\x10L\n\x06\x08\x04\x12\x02\x10L\n\x06\x08\x05\x12\x02\x10O'
        msg = protocol.encode_output_msg({'responses': [
            {'id': 1, 'response': [{'_uint8': ord('H'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}]},
            {'id': 2, 'response': [{'_uint8': ord('E'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}]},
            {'id': 3, 'response': [{'_uint8': ord('L'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}]},
            {'id': 4, 'response': [{'_uint8': ord('L'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}]},
            {'id': 5, 'response': [{'_uint8': ord('O'), 'instruction':None, '_uint16':None, '_uint32':None, '_uint64':None, '_int8':None, '_int16':None, '_int32':None, '_int64':None, '_float':None, '_double':None}]},
        ]})
        self.assertEqual(msg, raw_msg)
