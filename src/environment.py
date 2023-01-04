from stack import Stack
# Our global env
__env = []

# Our global stack
__stack = Stack()

def replace_environment(new_env):
    global __env
    __env = new_env

def clear_environment():
    global __env
    __env = []

def get_environment():
    return __env

def get_stack():
    return __stack

def clear_stack():
    global __stack
    __stack = Stack()