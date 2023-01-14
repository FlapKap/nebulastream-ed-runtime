from stack import Stack
import logging

__logger = logging.getLogger(__name__)

# Our global env
__env = []

# Our global stack
__stack = Stack()

def set_environment(new_env) -> None:
    global __env
    __env = new_env

def clear_environment() -> None:
    __logger.debug("clear_env called")
    global __env
    __env = []

def get_environment() -> list:
    return __env

def get_environment_copy() -> list:
    """
    returns shallow copy of the environment
    """
    return __env.copy()

def get_env_value(i):
    return __env[i] if len(__env) > i else None

def set_env_value(i, val) -> None:
    __logger.debug("set_env_value( {}, {})".format(i, val))
    dif = i-(len(__env)-1)
    if dif > 0:
        __env.extend([None]*dif)
    __env[i] = val

def get_stack() -> Stack:
    return __stack

def clear_stack() -> None:
    global __stack
    __stack = Stack()