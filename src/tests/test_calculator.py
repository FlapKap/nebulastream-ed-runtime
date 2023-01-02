import unittest

from expression import *

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Expression(bytes([ADD]),Stack([2,3]))
        calc()
        self.assertEqual(calc.stack.peek(), 5)

if __name__ == "__main__":
     unittest.main()
     