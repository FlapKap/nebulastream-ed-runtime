import unittest

from calculator import *

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator(bytes([ADD]),Stack([2,3]))
        calc.execute()
        self.assertEqual(calc.s.peek(), 5)

if __name__ == "__main__":
     unittest.main()
     