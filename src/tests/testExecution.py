from unittest import unittest
import execution
from operators import *
from expression import *
from datatypes import *
import environment

class TestExecution(unittest.TestCase):

    def setUp(self):
        environment.clear_environment()
        environment.clear_stack()

    def test_execute_query_with_result(self):
        query = Query([Map(Expression(bytes([CONST, INT8, 2, VAR, 0, MUL])),1)],[INT8])
        environment.set_env_value(0,4)
        res = execution._execute_query(query)

        self.assertEqual(res, [4,8])
    
    def test_execute_query_without_result(self):
        query = Query([Map(Expression(bytes([CONST, INT8, 2, VAR, 0, MUL])),1), Filter(Expression(bytes([VAR,1, CONST, INT8, 100, LT])))],[INT8])
        environment.set_env_value(0,4)
        res = execution._execute_query(query)

        self.assertEqual(res, None)
