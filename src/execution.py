import operators
import environment
import logging
logger = logging.getLogger(__name__)

def _execute_query(query: operators.Query):

    for op in query.operations:
        ## so far each operation gets its own stack
        ## TODO: this can probably be optimized away. Output of previous stack is input to next
        ## however cleaning the stack every time makes it a bit easier to reason about
        environment.clear_stack()
        cont = op()
        if not cont:
            return []

    return environment.get_environment_copy()

def execute_queries(queries: list[operators.Query], env)-> list[tuple[operators.Query,list]]:
    output = []
    for query in queries:
        logger.debug("environment initialized with: {}".format(env))
        environment.set_environment(env.copy())
        result = _execute_query(query)
        output.append((query,result))

    return output
