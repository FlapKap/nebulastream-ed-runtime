from unittest import unittest
from expression import *
import environment


class TestExpression(unittest.TestCase):

    def setUp(self):
        environment.clear_environment()
        environment.clear_stack()

    # region CONST
    def test_const_empty_stack(self):
        program = bytes([CONST, INT32]) + pack_type(INT32, 12345)
        ex = Expression(program)
        ex()
        self.assertEqual(ex.stack.peek(), 12345)

    def test_const_nonempty_stack(self):
        environment.get_stack().push(5)
        program = bytes([CONST, INT32]) + pack_type(INT32, 12345)
        ex = Expression(program)
        ex()
        self.assertEqual(ex.stack.pop(), 12345)
        self.assertEqual(ex.stack.pop(), 5)
    # endregion

    # region VAR
    def test_var(self):
        environment.replace_environment([1, 2, 3.0, 4.5])
        program = bytes([VAR, 0, VAR, 1, VAR, 2, VAR, 3])
        ex = Expression(program)
        ex()
        self.assertAlmostEqual(ex.stack.pop(), 4.5, delta=0.001)
        self.assertAlmostEqual(ex.stack.pop(), 3.0, delta=0.001)
        self.assertEqual(ex.stack.pop(), 2)
        self.assertEqual(ex.stack.pop(), 1)
    # endregion

    # region AND
    def test_and_11(self):
        environment.get_stack().push_multiple([1, 1])
        ex = Expression(bytes([AND]))
        ex()
        self.AssertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_10(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression(bytes([AND]))
        ex()
        self.AssertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_01(self):
        environment.get_stack().push_multiple([0, 1])
        ex = Expression(bytes([AND]))
        ex()
        self.AssertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_00(self):
        environment.get_stack().push_multiple([0, 0])
        ex = Expression(bytes([AND]))
        ex()
        self.AssertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region OR
    def test_or_11(self):
        environment.get_stack().push_multiple([1, 1])
        ex = Expression(bytes([OR]))
        ex()
        self.AssertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_10(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression(bytes([OR]))
        ex()
        self.AssertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_01(self):
        environment.get_stack().push_multiple([0, 1])
        ex = Expression(bytes([OR]))
        ex()
        self.AssertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_00(self):
        environment.get_stack().push_multiple([0, 0])
        ex = Expression(bytes([OR]))
        ex()
        self.AssertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region NOT
    def test_not_true(self):
        environment.get_stack().push(1)
        ex = Expression(bytes([NOT]))
        ex()
        self.AssertFalse(environment.get_stack().pop())

    def test_not_false(self):
        environment.get_stack().push(0)
        ex = Expression(bytes([NOT]))
        ex()
        self.AssertTrue(environment.get_stack().pop())
    # endregion

    # region LT
    def test_lt_true(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression(bytes([LT]))
        ex()
        self.assertTrue()
        self.assertEqual(len(environment.get_stack()), 0)

    def test_lt_false(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression(bytes([LT]))
        ex()
        self.assertFalse()
        self.assertEqual(len(environment.get_stack()), 0)

    def test_lt_equal_false(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression(bytes([LT]))
        ex()
        self.assertTrue()
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region GT
    def test_gt_true(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression(bytes([GT]))
        ex()
        self.assertTrue()
        self.assertEqual(len(environment.get_stack()), 0)

    def test_gt_false(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression(bytes([GT]))
        ex()
        self.assertFalse()
        self.assertEqual(len(environment.get_stack()), 0)

    def test_gt_equal_false(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression(bytes([GT]))
        ex()
        self.assertTrue()
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region EQ
    def test_eq_true(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression(bytes([EQ]))
        ex()
        self.assertTrue()
        self.assertEqual(len(environment.get_stack()), 0)

    def test_eq_false(self):
        environment.get_stack().push_multiple([21, 20])
        ex = Expression(bytes([EQ]))
        ex()
        self.assertFalse()
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region ADD

    def test_add_int_identity(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_add_int_inverse(self):
        environment.get_stack().push_multiple([2, -2])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertEqual(ex.stack.peek(), 0)

    def test_add_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_add_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertEqual(ex.stack.peek(), -5)

    def test_add_float_identity(self):
        environment.get_stack().push_multiple([1.0, 0.0])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_add_float_inverse(self):
        environment.get_stack().push_multiple([2.0, -2.0])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertEqual(ex.stack.peek(), 0.0, delta=0.001)

    def test_add_float_positive(self):
        environment.get_stack().push_multiple([2.5, 3.3])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 5.8, delta=0.001)

    def test_add_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.9, delta=0.001)

    def test_add_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression(bytes([ADD]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -6.0, delta=0.001)
    # endregion

    # region SUB
    def test_sub_int_identity(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_sub_int_inverse(self):
        environment.get_stack().push_multiple([2, 2])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertEqual(ex.stack.peek(), 0)

    def test_sub_int_positive(self):
        environment.get_stack().push_multiple([2, 3])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertEqual(ex.stack.peek(), -1)

    def test_sub_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertEqual(ex.stack.peek(), -5)

    def test_sub_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_sub_float_identity(self):
        environment.get_stack().push_multiple([1.0, 0.0])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_sub_float_inverse(self):
        environment.get_stack().push_multiple([2.0, -2.0])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 0.0, delta=0.001)

    def test_sub_float_positive(self):
        environment.get_stack().push_multiple([2.5, 3.3])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 5.8, delta=0.001)

    def test_sub_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -3.1, delta=0.001)

    def test_sub_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression(bytes([SUB]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.5, delta=0.001)
    # endregion

    # region MUL
    def test_mul_int_identity(self):
        environment.get_stack().push_multiple([2, 1])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertEqual(ex.stack.peek(), 2)

    def test_mul_float_identity(self):
        environment.get_stack().push_multiple([2.0, 1.0])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.0)

    def test_mul_float_inverse(self):
        environment.get_stack().push_multiple([2, 0.5])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_mul_int_positive(self):
        environment.get_stack().push_multiple([2, 3])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertEqual(ex.stack.peek(), 6)

    def test_mul_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertEqual(ex.stack.peek(), -6)

    def test_mul_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertEqual(ex.stack.peek(), 6)

    def test_mul_float_positive(self):
        environment.get_stack().push_multiple([2.5, 3.3])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 8.25, delta=0.001)

    def test_mul_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -0.3, delta=0.001)

    def test_mul_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression(bytes([MUL]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 8.625, delta=0.001)
    # endregion

    # region DIV
    def test_div_float_identity(self):
        environment.get_stack().push_multiple([2.0, 1.0])
        ex = Expression(bytes([DIV]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.0, delta=0.001)

    def test_div_float_inverse(self):
        environment.get_stack().push_multiple([2.0, 2.0])
        ex = Expression(bytes([DIV]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_div_float_positive(self):
        environment.get_stack().push_multiple([2.5, 5.0])
        ex = Expression(bytes([DIV]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 0.5, delta=0.001)

    def test_div_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3.0])
        ex = Expression(bytes([DIV]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -0.03, delta=0.001)

    def test_div_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -0.5])
        ex = Expression(bytes([DIV]))
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 5.0, delta=0.001)

    def test_div_divide_by_zero(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression(bytes([DIV]))
        with self.assertRaises(ZeroDivisionError):
            ex()  # TODO: is this actually the handling we want?
    # endregion

    # region MOD
    def test_mod_int_0(self):
        environment.get_stack().push_multiple([10, 0])
        ex = Expression(bytes([MOD]))
        with self.assertRaises(ZeroDivisionError):
            ex()  # TODO: is this actually the handling we want?

    def test_mod_int_1(self):
        environment.get_stack().push_multiple([10, 1])
        ex = Expression(bytes([MOD]))
        ex()
        self.assertEqual(ex.stack.pop(), 0)

    def test_mod_int_self(self):
        environment.get_stack().push_multiple([10, 10])
        ex = Expression(bytes([MOD]))
        ex()
        self.assertEqual(ex.stack.pop(), 0)

    def test_mod_int_positive(self):
        environment.get_stack().push_multiple([10, 3])
        ex = Expression(bytes([MOD]))
        ex()
        self.assertEqual(ex.stack.pop(), 1)

    # TODO: mod with negative quotient behave different in python than in C. Do we wish to replicate C behaviour?
    # endregion
