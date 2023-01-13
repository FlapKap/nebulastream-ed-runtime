from unittest import unittest
from datatypes import *
import environment


class TestDataTypes(unittest.TestCase):

    def test_pack_type(self):
        self.assertEqual(pack_type(INT8, -14), b'\xf2')
        self.assertEqual(pack_type(UINT8, 14), b'\x0e')
        self.assertEqual(pack_type(INT16, -12345), b'\xc7\xcf')
        self.assertEqual(pack_type(UINT16, 12345), b'90')
        self.assertEqual(pack_type(INT32, -123456789), b'\xeb2\xa4\xf8')
        self.assertEqual(pack_type(UINT32, 123456789), b'\x15\xcd[\x07')
        self.assertEqual(pack_type(INT64, -2**56),
                         b'\x00\x00\x00\x00\x00\x00\x00\xff')
        self.assertEqual(pack_type(UINT64, 2**56),
                         b'\x00\x00\x00\x00\x00\x00\x00\x01')
        self.assertEqual(pack_type(FLOAT, 3.14), b'\xc3\xf5H@')
        self.assertEqual(pack_type(DOUBLE, 3.14), b'\x00\x00\x00`\xb8\x1e\t@')

    def test_pack_array_same_type(self):
        testarray = [1, 2, 3, 4, 5]
        self.assertEqual(
            pack_array((INT8, INT8, INT8, INT8, INT8), testarray),
            b'\x01\x02\x03\x04\x05'
        )

        testarray = [123456784, 123456785, 123456786, 123456787, 123456788]
        self.assertEqual(
            pack_array((INT32, INT32, INT32, INT32, INT32), testarray),
            b'\x10\xcd[\x07\x11\xcd[\x07\x12\xcd[\x07\x13\xcd[\x07\x14\xcd[\x07'
        )

    def test_pack_array_different_types(self):
        testtypes = (INT8, UINT8, INT16, UINT16, INT32,
                     UINT32, INT64, UINT64, FLOAT, DOUBLE)
        testarray = [-14, 14, -12345, 12345, -123456789,
                     123456789, -2**56, 2**56, 3.14, 3.14]
        self.assertEqual(
            pack_array(testtypes, testarray),
            (b'\xf2' + b'\x0e' + b'\xc7\xcf' + b'90' + b'\xeb2\xa4\xf8' +
             b'\x15\xcd[\x07' + b'\x00\x00\x00\x00\x00\x00\x00\xff' + b'\x00\x00\x00\x00\x00\x00\x00\x01' +
             b'\xc3\xf5H@' + b'\x00\x00\x00`\xb8\x1e\t@')
        )
