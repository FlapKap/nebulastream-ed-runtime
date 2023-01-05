from micropython import const

class Operator:

    def __call__(self, inp=None):
        raise Exception("operator doesn't implement callable")


class Map(Operator):

    def __init__(self, function):
        self.f = function

    def __call__(self, *args, **kwargs):

        return self.f(*args, **kwargs)

class Filter(Operator):
    def __init__(self, predicate):
        self.f = predicate

    def __call__(self, *args):
        def compute():
            if self.f(*args):
                if len(args) == 1:
                    return args[0]
                
                return args
            return None
            
        return compute()

# windows
## 2 types of windows are supported. Sliding and tumbling
## for each window an aggreation function is needed. This is the actual output of the window
## Here we support min, max, sum, avg, count
class WindowAggregationType:
    MIN = const(0)
    MAX = const(1)
    SUM = const(2)
    AVG = const(3)
    COUNT = const(4)

class WindowSizeType:
    TIMEBASED = const(0)
    COUNTBASED = const(1)

class TumblingWindow(Operator):
    """
    Window operator. A window has a type and an aggregation function
    """
    def __init__(self, size_type, aggregation_type, size):
        self.__size_type = size_type
        self.__agg_type = aggregation_type
        self.__size = size
        