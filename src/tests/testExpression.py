from unittest import unittest
from expression import *
import environment
from datatypes import *


class TestExpression(unittest.TestCase):

    def setUp(self):
        environment.clear_environment()
        environment.clear_stack()

    # region CONST
    def test_const_empty_stack(self):
        program = [CONST, 12345]
        ex = Expression(program)
        res = ex()
        self.assertEqual(res, 12345)

    def test_const_nonempty_stack(self):
        environment.get_stack().push(5)
        program = [CONST, 12345]
        ex = Expression(program)
        ex()
        self.assertEqual(ex.stack.pop(), 12345)
        self.assertEqual(ex.stack.pop(), 5)
    # endregion

    # region VAR
    def test_var(self):
        environment.set_environment([1, 2, 3.0, 4.5])
        program = [VAR, 0, VAR, 1, VAR, 2, VAR, 3]
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
        ex = Expression([AND])
        ex()
        self.assertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_10(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([AND])
        ex()
        self.assertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_01(self):
        environment.get_stack().push_multiple([0, 1])
        ex = Expression([AND])
        ex()
        self.assertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_and_00(self):
        environment.get_stack().push_multiple([0, 0])
        ex = Expression([AND])
        ex()
        self.assertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region OR
    def test_or_11(self):
        environment.get_stack().push_multiple([1, 1])
        ex = Expression([OR])
        ex()
        self.assertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_10(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([OR])
        ex()
        self.assertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_01(self):
        environment.get_stack().push_multiple([0, 1])
        ex = Expression([OR])
        ex()
        self.assertTrue(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)

    def test_or_00(self):
        environment.get_stack().push_multiple([0, 0])
        ex = Expression([OR])
        ex()
        self.assertFalse(environment.get_stack().pop())
        self.assertEqual(len(environment.get_stack()), 0)
    # endregion

    # region NOT
    def test_not_true(self):
        environment.get_stack().push(1)
        ex = Expression([NOT])
        ex()
        self.assertFalse(environment.get_stack().pop())

    def test_not_false(self):
        environment.get_stack().push(0)
        ex = Expression([NOT])
        ex()
        self.assertTrue(environment.get_stack().pop())
    # endregion

    # region LT
    def test_lt_true(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression([LT])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_lt_false(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression([LT])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_lt_equal_false(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression([LT])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)
    # endregion

    # region GT
    def test_gt_true(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression([GT])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_gt_false(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression([GT])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_gt_equal_false(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression([GT])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)
    # endregion

    # region EQ
    def test_eq_true(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression([EQ])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_eq_false(self):
        environment.get_stack().push_multiple([21, 20])
        ex = Expression([EQ])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)
    # endregion

    # region ADD

    def test_add_int_identity(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([ADD])
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_add_int_inverse(self):
        environment.get_stack().push_multiple([2, -2])
        ex = Expression([ADD])
        ex()
        self.assertEqual(ex.stack.peek(), 0)

    def test_add_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression([ADD])
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_add_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression([ADD])
        ex()
        self.assertEqual(ex.stack.peek(), -5)

    def test_add_float_identity(self):
        environment.get_stack().push_multiple([1.0, 0.0])
        ex = Expression([ADD])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_add_float_inverse(self):
        environment.get_stack().push_multiple([2.0, -2.0])
        ex = Expression([ADD])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 0.0, delta=0.001)

    def test_add_float_positive(self):
        environment.get_stack().push_multiple([2.5, 3.3])
        ex = Expression([ADD])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 5.8, delta=0.001)

    def test_add_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression([ADD])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.9, delta=0.001)

    def test_add_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression([ADD])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -6.0, delta=0.001)
    # endregion

    # region SUB
    def test_sub_int_identity(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([SUB])
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_sub_int_inverse(self):
        environment.get_stack().push_multiple([2, 2])
        ex = Expression([SUB])
        ex()
        self.assertEqual(ex.stack.peek(), 0)

    def test_sub_int_positive(self):
        environment.get_stack().push_multiple([2, 3])
        ex = Expression([SUB])
        ex()
        self.assertEqual(ex.stack.peek(), -1)

    def test_sub_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression([SUB])
        ex()
        self.assertEqual(ex.stack.peek(), -5)

    def test_sub_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression([SUB])
        ex()
        self.assertEqual(ex.stack.peek(), 1)

    def test_sub_float_identity(self):
        environment.get_stack().push_multiple([1.0, 0.0])
        ex = Expression([SUB])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_sub_float_inverse(self):
        environment.get_stack().push_multiple([2.0, 2.0])
        ex = Expression([SUB])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 0.0, delta=0.001)

    def test_sub_float_positive(self):
        environment.get_stack().push_multiple([1.5, 2.5])
        ex = Expression([SUB])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -1.0, delta=0.001)

    def test_sub_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression([SUB])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -3.1, delta=0.001)

    def test_sub_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression([SUB])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)
    # endregion

    # region MUL
    def test_mul_int_identity(self):
        environment.get_stack().push_multiple([2, 1])
        ex = Expression([MUL])
        ex()
        self.assertEqual(ex.stack.peek(), 2)

    def test_mul_float_identity(self):
        environment.get_stack().push_multiple([2.0, 1.0])
        ex = Expression([MUL])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.0)

    def test_mul_float_inverse(self):
        environment.get_stack().push_multiple([2, 0.5])
        ex = Expression([MUL])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_mul_int_positive(self):
        environment.get_stack().push_multiple([2, 3])
        ex = Expression([MUL])
        ex()
        self.assertEqual(ex.stack.peek(), 6)

    def test_mul_int_negative(self):
        environment.get_stack().push_multiple([-2, 3])
        ex = Expression([MUL])
        ex()
        self.assertEqual(ex.stack.peek(), -6)

    def test_mul_int_double_negative(self):
        environment.get_stack().push_multiple([-2, -3])
        ex = Expression([MUL])
        ex()
        self.assertEqual(ex.stack.peek(), 6)

    def test_mul_float_positive(self):
        environment.get_stack().push_multiple([2.5, 3.3])
        ex = Expression([MUL])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 8.25, delta=0.001)

    def test_mul_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression([MUL])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -0.3, delta=0.001)

    def test_mul_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -3.5])
        ex = Expression([MUL])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 8.75, delta=0.001)
    # endregion

    # region DIV
    def test_div_float_identity(self):
        environment.get_stack().push_multiple([2.0, 1.0])
        ex = Expression([DIV])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 2.0, delta=0.001)

    def test_div_float_inverse(self):
        environment.get_stack().push_multiple([2.0, 2.0])
        ex = Expression([DIV])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 1.0, delta=0.001)

    def test_div_float_positive(self):
        environment.get_stack().push_multiple([2.5, 5.0])
        ex = Expression([DIV])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 0.5, delta=0.001)

    def test_div_float_negative(self):
        environment.get_stack().push_multiple([-0.1, 3])
        ex = Expression([DIV])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), -0.03333, delta=0.001)

    def test_div_float_double_negative(self):
        environment.get_stack().push_multiple([-2.5, -0.5])
        ex = Expression([DIV])
        ex()
        self.assertAlmostEqual(ex.stack.peek(), 5.0, delta=0.001)

    def test_div_divide_by_zero(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([DIV])
        with self.assertRaises(ZeroDivisionError):
            ex()  # TODO: is this actually the handling we want?
    # endregion

    # region MOD
    def test_mod_int_0(self):
        environment.get_stack().push_multiple([10, 0])
        ex = Expression([MOD])
        with self.assertRaises(ZeroDivisionError):
            ex()  # TODO: is this actually the handling we want?

    def test_mod_int_1(self):
        environment.get_stack().push_multiple([10, 1])
        ex = Expression([MOD])
        ex()
        self.assertEqual(ex.stack.pop(), 0)

    def test_mod_int_self(self):
        environment.get_stack().push_multiple([10, 10])
        ex = Expression([MOD])
        ex()
        self.assertEqual(ex.stack.pop(), 0)

    def test_mod_int_positive(self):
        environment.get_stack().push_multiple([3, 10])
        ex = Expression([MOD])
        ex()
        self.assertEqual(ex.stack.pop(), 3)

    # TODO: mod with negative quotient behave different in python than in C. Do we wish to replicate C behaviour?
    # endregion

    # region LT
    def test_lteq_true(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression([LTEQ])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_lteq_false(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression([LTEQ])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_lteq_equal_true(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression([LTEQ])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)
    # endregion

    # region GT
    def test_gteq_true(self):
        environment.get_stack().push_multiple([20, 10])
        ex = Expression([GTEQ])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_gteq_false(self):
        environment.get_stack().push_multiple([10, 20])
        ex = Expression([GTEQ])
        res = ex()
        self.assertFalse(res)
        self.assertEqual(len(environment.get_stack()), 1)

    def test_gteq_equal_true(self):
        environment.get_stack().push_multiple([20, 20])
        ex = Expression([GTEQ])
        res = ex()
        self.assertTrue(res)
        self.assertEqual(len(environment.get_stack()), 1)
    # endregion

    # region LOG
    def test_log_one(self):
        environment.get_stack().push(1)
        ex = Expression([LOG])
        res = ex()
        self.assertAlmostEqual(0, res, delta=0.00001)

    def test_log_ten(self):
        environment.get_stack().push(10)
        ex = Expression([LOG])
        res = ex()
        self.assertAlmostEqual(2.3, res, delta=0.01)
    # endregion

    # # region LOG2
    # def test_log2_one(self):
    #     environment.get_stack().push(1)
    #     ex = Expression([LOG2])
    #     res = ex()
    #     self.assertAlmostEqual(0, res, delta=0.00001)

    # def test_log2_256(self):
    #     environment.get_stack().push(256)
    #     ex = Expression([LOG2])
    #     res = ex()
    #     self.assertAlmostEqual(8.0, res, delta=0.0001)
    # # endregion

    # # region LOG10
    # def test_log10_one(self):
    #     environment.get_stack().push(1)
    #     ex = Expression([LOG10])
    #     res = ex()
    #     self.assertAlmostEqual(0, res, delta=0.00001)

    # def test_log10_1000(self):
    #     environment.get_stack().push(1000)
    #     ex = Expression([LOG10])
    #     res = ex()
    #     self.assertAlmostEqual(3.0, res, delta=0.0001)
    # # endregion

    # region POW
    def test_pow_zero_zero(self):
        environment.get_stack().push_multiple([0, 0])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(1, res, delta=0.00001)

    def test_pow_zero_one(self):
        environment.get_stack().push_multiple([0, 1])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(0, res, delta=0.00001)

    def test_pow_one_zero(self):
        environment.get_stack().push_multiple([1, 0])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(1, res, delta=0.0001)

    def test_pow_one_one(self):
        environment.get_stack().push_multiple([1, 1])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(1, res, delta=0.0001)

    def test_pow_two_eight(self):
        environment.get_stack().push_multiple([2, 8])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(256, res, delta=0.0001)

    def test_pow_two_neg_two(self):
        environment.get_stack().push_multiple([2, -2])
        ex = Expression([POW])
        res = ex()
        self.assertAlmostEqual(0.25, res, delta=0.0001)
    # endregion

    # region SQRT
    def test_sqrt_zero(self):
        environment.get_stack().push(0)
        ex = Expression([SQRT])
        res = ex()
        self.assertAlmostEqual(0, res, delta=0.00001)

    def test_sqrt_one(self):
        environment.get_stack().push(1)
        ex = Expression([SQRT])
        res = ex()
        self.assertAlmostEqual(1, res, delta=0.00001)

    def test_sqrt_25(self):
        environment.get_stack().push(25)
        ex = Expression([SQRT])
        res = ex()
        self.assertAlmostEqual(5, res, delta=0.00001)
    # endregion

    # region EXP
    def test_exp_zero(self):
        environment.get_stack().push(0)
        ex = Expression([EXP])
        res = ex()
        self.assertAlmostEqual(1, res, delta=0.00001)

    def test_exp_one(self):
        environment.get_stack().push(1)
        ex = Expression([EXP])
        res = ex()
        self.assertAlmostEqual(2.7182, res, delta=0.001)

    def test_exp_neg_one(self):
        environment.get_stack().push(-1)
        ex = Expression([EXP])
        res = ex()
        self.assertAlmostEqual(0.367879441, res, delta=0.00001)
    # endregion

    # region CEIL
    def test_ceil_zero(self):
        environment.get_stack().push(0)
        ex = Expression([CEIL])
        res = ex()
        self.assertEqual(0, res)

    def test_ceil_zero_point_one(self):
        environment.get_stack().push(0.1)
        ex = Expression([CEIL])
        res = ex()
        self.assertEqual(1, res)
    # endregion

    # region FLOOR
    def test_floor_zero(self):
        environment.get_stack().push(0)
        ex = Expression([FLOOR])
        res = ex()
        self.assertEqual(0, res)

    def test_floor_zero_point_one(self):
        environment.get_stack().push(0.1)
        ex = Expression([FLOOR])
        res = ex()
        self.assertEqual(0, res)
    # endregion

    # region ROUND
    def test_round_zero(self):
        environment.get_stack().push(0)
        ex = Expression([ROUND])
        res = ex()
        self.assertEqual(0, res)

    def test_round_zero_point_one(self):
        environment.get_stack().push(0.1)
        ex = Expression([ROUND])
        res = ex()
        self.assertEqual(0, res)

    def test_round_zero_point_five(self):
        environment.get_stack().push(0.5)
        ex = Expression([ROUND])
        res = ex()
        self.assertEqual(0, res)  # python...

    def test_round_one_point_five(self):
        environment.get_stack().push(1.5)
        ex = Expression([ROUND])
        res = ex()
        self.assertEqual(2, res)  # python...

    def test_round_zero_point_six(self):
        environment.get_stack().push(0.6)
        ex = Expression([ROUND])
        res = ex()
        self.assertEqual(1, res)
    # endregion

    # region ABS
    def test_abs_zero(self):
        environment.get_stack().push(0)
        ex = Expression([ABS])
        res = ex()
        self.assertEqual(0, res)

    def test_abs_negative_one(self):
        environment.get_stack().push(-1)
        ex = Expression([ABS])
        res = ex()
        self.assertEqual(1, res)
    # endregion
# # arithmetic


# ABS = const(22)
