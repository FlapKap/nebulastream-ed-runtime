from unittest import unittest
from operators import *


class TestOperators(unittest.TestCase):

    def test_map_operator(self):
        op = Map(lambda x: x)
        self.assertEqual(op(3), 3)

    def test_filter_operator_true(self):
        op = Filter(lambda x: x == 3)
        self.assertEqual(op(3), 3)

    def test_filter_operator_false(self):
        op = Filter(lambda x: x == 3)
        self.assertFalse(op(2))

    def test_window_tumbling_min(self):
        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.MIN, 3)
        self.assertEqual(op(3), 3)
        self.assertEqual(op(4), 3)
        self.assertEqual(op(2), 2)
        self.assertEqual(op(5), 5)  # we go into next window

    def test_window_tumbling_max(self):
        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.MAX, 3)
        self.assertEqual(op(3), 3)
        self.assertEqual(op(4), 4)
        self.assertEqual(op(2), 4)
        self.assertEqual(op(3), 3)  # we go into next window

    def test_window_tumbling_sum(self):
        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.SUM, 3)
        self.assertEqual(op(1), 1)
        self.assertEqual(op(2), 3)
        self.assertEqual(op(3), 6)
        self.assertEqual(op(4), 4)  # we go into next window

    def test_window_tumbling_avg(self):
        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.AVG, 3)
        self.assertEqual(op(3), 3)
        self.assertEqual(op(4), 3.5)
        self.assertEqual(op(14), 7)
        self.assertEqual(op(3), 3)  # we go into next window

    def test_window_tumbling_count(self):
        op = TumblingWindow(WindowSizeType.COUNTBASED,
                            WindowAggregationType.COUNT, 3)
        self.assertEqual(op(3), 1)
        self.assertEqual(op(4), 2)
        self.assertEqual(op(14), 3)
        self.assertEqual(op(3), 1)  # we go into next window
