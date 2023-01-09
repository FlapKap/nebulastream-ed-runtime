from unittest import unittest
import protocol
from expression import CONST, INT8, INT16, INT32, MUL, LT, GT
from operators import WindowAggregationType, WindowSizeType

class TestProtocol(unittest.TestCase):

    def test_empty_msg(self):
        raw_msg = b''
        msg = protocol.decode_input_msg(raw_msg)

        expected = {"operations": ()}
        self.assertEqual(msg, expected)

    def test_map_msg(self):
        raw_msg = b'\n\n\n\x08\n\x06\n\x04\x00\x04\x08\n'
        msg = protocol.decode_input_msg(raw_msg)

        expected = {'operations':
                    ({'map': {'function': {'instructions': bytes([CONST, INT32, 8, MUL])}}, 'filter': None, 'window':None},)}
        self.assertEqual(msg, expected)

    def test_filter_msg(self):
        raw_msg = b'\n\n\x12\x08\n\x06\n\x04\x00\x00\x08\x05'
        msg = protocol.decode_input_msg(raw_msg)

        expected = {'operations':
                    ({'map': None,'window':None, 'filter': {'predicate': {'instructions': bytes([CONST, INT8, 8, LT])}}},)}
        self.assertEqual(msg, expected)

    def test_filter_map_msg(self):
        raw_msg = b'\n\n\n\x08\n\x06\n\x04\x00\x04\x08\n\n\n\x12\x08\n\x06\n\x04\x00\x022\x06'
        msg = protocol.decode_input_msg(raw_msg)

        expected = {'operations': (
            {'filter': None, 'window':None, 'map': {'function': {
                'instructions': bytes([CONST, INT32, 8, MUL])}}},
            {'map': None, 'window':None, 'filter': {'predicate': {'instructions': bytes([CONST, INT16, 50, GT])}}})}
        self.assertEqual(msg, expected)
    
    def test_window_msg(self):
        raw_msg = b'\n\x08\x1a\x06\x08\x03\x10\x01\x18\x04'
        msg = protocol.decode_input_msg(raw_msg)
        expected = {'operations': (
            {'filter':None,
            'map':None,
            'window': {'size': 3, 'sizeType': WindowSizeType.COUNTBASED, 'aggType': WindowAggregationType.COUNT}},)}
        self.assertEqual(msg, expected)
