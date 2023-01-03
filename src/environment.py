# Our global env
__env = []


def replace_environment(new_env):
    global __env
    __env = new_env


def get_environment():
    return __env
