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
        query = Query([Map(Expression([CONST, 2, VAR, 0, MUL]),1)])
        environment.set_env_value(0,4)
        res = execution._execute_query(query)

        self.assertEqual(res, [4,8])
    
    def test_execute_query_without_result(self):
        query = Query([Map(Expression([CONST, 2, VAR, 0, MUL]),1), Filter(Expression([VAR,1, CONST, 2, LT]))])
        environment.set_env_value(0,4)
        res = execution._execute_query(query)

        self.assertEqual(res, None)
    
    def test_execute_quries_single_result(self):
        queries = [Query([Map(Expression([CONST, 2, VAR, 0, MUL]),1)])]
        res = execution.execute_queries(queries,[4])
        self.assertEqual(res, [[4,8]])
    
    def test_execute_queries_multiple_results(self):
        queries = [
            Query([Map(Expression([CONST, 2, VAR, 0, MUL]),1), Filter(Expression([VAR,1, CONST, 2, LT]))],),
            Query([Map(Expression([CONST, 2, VAR, 0, MUL]),1)])
            ]
        res = execution.execute_queries(queries, [4])
        self.assertEqual(res, [None,[4,8]])
