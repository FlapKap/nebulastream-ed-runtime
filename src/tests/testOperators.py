from unittest import unittest
from operators import *
import environment
from expression import Expression, CONST, ADD, SUB, MUL
from datatypes import INT8

class TestOperators(unittest.TestCase):

    def setUp(self):
        environment.clear_environment()
        environment.clear_stack()

    def test_map_operator(self):
        #environment.set_env_value(0, 3)
        expected = 3
        op = Map(lambda : expected, 0)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(0), expected)

    def test_map_expression(self):
        op = Map(
            # 2 3 + 42 12 - *
            Expression([CONST, 2, CONST, 3, ADD, CONST, 42, CONST, 12, SUB, MUL]),
            0
        )
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(0),150)

    def test_filter_operator_true(self):
        op = Filter(lambda : True)
        self.assertTrue(op())

    def test_filter_operator_false(self):
        op = Filter(lambda : False)
        self.assertFalse(op())

    # region window
    # for window operators we need to test that they
    # return true only when a window is finished
    # that 
    def test_window_tumbling_min(self):
        start = 0
        end = 1
        result = 2
        read = 3

        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.MIN, 3,start,end,result,read)
        environment.set_env_value(read, 3)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 4)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 2)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 2)
        self.assertEqual(environment.get_env_value(start), 0)
        self.assertEqual(environment.get_env_value(end), 2)

        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 10)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 8)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 5)
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

    def test_window_tumbling_max(self):
        start = 0
        end = 1
        result = 2
        read = 3

        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.MAX, 3,start,end,result,read)
        environment.set_env_value(read, 3)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 4)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 2)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 4)
        self.assertEqual(environment.get_env_value(start), 0)
        self.assertEqual(environment.get_env_value(end), 2)
        
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 10)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 8)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 10)
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window


    def test_window_tumbling_sum(self):
        start = 0
        end = 1
        result = 2
        read = 3

        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.SUM, 3,start,end,result,read)
        environment.set_env_value(read, 3)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 4)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 2)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 9)
        self.assertEqual(environment.get_env_value(start), 0)
        self.assertEqual(environment.get_env_value(end), 2)
        
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 10)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 8)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 23)
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

    def test_window_tumbling_avg(self):
        start = 0
        end = 1
        result = 2
        read = 3

        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.AVG, 3,start,end,result,read)
        environment.set_env_value(read, 3)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 4)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 14)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 7)
        self.assertEqual(environment.get_env_value(start), 0)
        self.assertEqual(environment.get_env_value(end), 2)
        
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 10)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 0)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 5)
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window


    def test_window_tumbling_count(self):
        start = 0
        end = 1
        result = 2
        read = 3

        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.COUNT, 3,start,end,result,read)
        environment.set_env_value(read, 3)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 4)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 2)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 3)
        self.assertEqual(environment.get_env_value(start), 0)
        self.assertEqual(environment.get_env_value(end), 2)
        
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window

        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 10)
        self.assertFalse(op())
        self.assertEqual(environment.get_env_value(result), None)

        environment.set_env_value(read, 8)
        self.assertTrue(op())
        self.assertEqual(environment.get_env_value(result), 3)
        environment.set_env_value(read, 5)
        self.assertFalse(op())  # we go into next window
    # endregion