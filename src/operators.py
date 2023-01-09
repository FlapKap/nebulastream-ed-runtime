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
# 2 types of windows are supported. Sliding and tumbling
# for each window an aggreation function is needed. This is the actual output of the window
# Here we support min, max, sum, avg, count


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
    TODO: implement time-based
    """

    def __init__(self, size_type, aggregation_type, size):
        self.__size_type = size_type
        self.__agg_type = aggregation_type
        self.__size = size
        self.__state_count = 0

        self.__state_value = None

    def __call__(self, e):
        # first reset state count and value if count reached
        if self.__state_count == self.__size:
            self.__state_count = 0
            self.__state_value = None
        
        # incr call count
        self.__state_count += 1


        # handle the different window types
        ## for each different case we also have to handle if its the first call
        ## i.e. if value is None, how do we initialize. Right now its spread out
        ## which is ugly but works
        if self.__agg_type == WindowAggregationType.MIN:
            self.__state_value = e if self.__state_value is None else min(e, self.__state_value)
            return self.__state_value
        if self.__agg_type == WindowAggregationType.MAX:
            self.__state_value = e if self.__state_value is None else max(e, self.__state_value)
            return self.__state_value
        if self.__agg_type == WindowAggregationType.SUM:
            if self.__state_value is None:
                self.__state_value = 0
            self.__state_value += e
            return self.__state_value
        if self.__agg_type == WindowAggregationType.AVG:
            if self.__state_value is None:
                self.__state_value = 0
            self.__state_value += e
            return self.__state_value / self.__state_count
        if self.__agg_type == WindowAggregationType.COUNT:
            return self.__state_count
