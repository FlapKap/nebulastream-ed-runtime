from unittest import unittest
import protocol
from expression import CONST, INT8, INT16, INT32, MUL, LT, GT, Expression
from operators import *


class TestProtocol(unittest.TestCase):

    def test_empty_msg(self):
        raw_msg = b''
        msg = protocol.decode_input_msg(raw_msg)

        expected = []
        self.assertEqual(msg, expected)

    def test_map_msg(self):
        raw_msg = b'\n\n\n\x08\n\x06\n\x04\x00\x04\x08\n'
        op = protocol.decode_input_msg(raw_msg)[0]

        expected = Map(Expression(bytes([CONST, INT32, 8, MUL])),0)
        self.assertEqual(op, expected)

    def test_filter_msg(self):
        raw_msg = b'\n\n\x12\x08\n\x06\n\x04\x00\x00\x08\x05'
        op = protocol.decode_input_msg(raw_msg)[0]

        expected = Filter(Expression(bytes([CONST, INT8, 8, LT])))
        self.assertEqual(op, expected)

    def test_map_filter_msg(self):
        raw_msg = b'\n\n\n\x08\n\x06\n\x04\x00\x04\x08\n\n\n\x12\x08\n\x06\n\x04\x00\x022\x06'
        ops = protocol.decode_input_msg(raw_msg)

        expected = [
            Map(Expression(bytes([CONST, INT32, 8, MUL])), 0),
            Filter(Expression(bytes([CONST, INT16, 50, GT])))
        ]

        self.assertEqual(ops, expected)

    def test_window_msg(self):
        raw_msg = b'\n\x0e\x1a\x0c\x08\x03\x10\x01\x18\x04(\x010\x028\x03'
        op = protocol.decode_input_msg(raw_msg)[0]
        expected = TumblingWindow(WindowSizeType.COUNTBASED, WindowAggregationType.COUNT,3,0,1,2,3)
        
        self.assertEqual(op, expected)
    
    def test_output_msg(self):
        raw_msg = b'\n\x07\n\x05HELLO\n\x07\n\x05THERE\n\t\n\x07GENERAL\n\x08\n\x06KENOBI'
        msg = protocol.encode_output_msg({'values': [
            {'value': b'HELLO'},
            {'value': b'THERE'},
            {'value': b'GENERAL'},
            {'value': b'KENOBI'}
            ]})
        self.assertEqual(msg, raw_msg)