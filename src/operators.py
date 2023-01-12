from micropython import const
import environment


class Operator:

    def __call__(self) -> bool:
        """
        execute the operator. The output is a bool that indicates whether or not the pipeline should continue
        """
        raise Exception("operator doesn't implement callable")


class Map(Operator):

    def __init__(self, function, attribute):
        self.f = function
        self.attribute = attribute

    def __call__(self):
        environment.set_env_value(self.attribute, self.f())
        return True

    def __eq__(self, __o):
        if isinstance(__o, Map):
            return self.attribute == __o.attribute and self.f == __o.f
        return False

    def __str__(self):
        return "Map({}, {})".format(self.f, self.attribute)

class Filter(Operator):
    def __init__(self, predicate):
        self.f = predicate

    def __call__(self):
        return self.f()

    def __eq__(self, __o):
        if isinstance(__o, Filter):
            return self.f == __o.f
        return False


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

    def __init__(self, sizeType, aggregationType, size, startAttribute, endAttribute, resultAttribute, readAttribute):
        self.__size_type = sizeType
        self.__agg_type = aggregationType
        self.__size = size
        self.__start_attribute = startAttribute
        self.__end_attribute = endAttribute
        self.__result_attribute = resultAttribute
        self.__read_attribute = readAttribute

        self.__call_count = 0  # total calls since start of init

        self.__state = {}

        self.__agg_functions = {
            WindowAggregationType.MIN:   self.__min,
            WindowAggregationType.MAX:   self.__max,
            WindowAggregationType.AVG:   self.__avg,
            WindowAggregationType.SUM:   self.__sum,
            WindowAggregationType.COUNT: self.__count,
        }
        self.__f = self.__agg_functions[self.__agg_type]

    def __eq__(self, __o):
        if isinstance(__o, TumblingWindow):
            return (
                    self.__size_type        == __o.__size_type and 
                    self.__agg_type         == __o.__agg_type and
                    self.__size             == __o.__size and 
                    self.__start_attribute  == __o.__start_attribute and
                    self.__end_attribute    == __o.__end_attribute and
                    self.__read_attribute   == __o.__read_attribute and
                    self.__call_count       == __o.__call_count and
                    self.__state            == __o.__state
                    )
        return False

    # region aggfuncs
    # These functions handle the agg computation itself

    def __min(self):
        value = environment.get_env_value(self.__read_attribute)

        if "running_min" not in self.__state:
            self.__state["running_min"] = value
        else:
            self.__state["running_min"] = min(
                value, self.__state["running_min"])
            return self.__state["running_min"]

    def __max(self):
        value = environment.get_env_value(self.__read_attribute)

        if "running_max" not in self.__state:
            self.__state["running_max"] = value
        else:
            self.__state["running_max"] = max(
                value, self.__state["running_max"])
        return self.__state["running_max"]

    def __sum(self):
        value = environment.get_env_value(self.__read_attribute)
        if "running_sum" not in self.__state:
            self.__state["running_sum"] = value
        else:
            self.__state["running_sum"] += value
        return self.__state["running_sum"]

    def __avg(self):
        if "running_sum" not in self.__state:
            self.__state["running_sum"] = environment.get_env_value(
                self.__read_attribute)
        if "running_count" not in self.__state:
            self.__state["running_count"] = 1
        else:
            self.__state["running_sum"] += environment.get_env_value(
                self.__read_attribute)
            self.__state["running_count"] += 1
        return self.__state["running_sum"] / self.__state["running_count"]

    def __count(self):
        return (self.__call_count % self.__size) + 1

    # endregion

    def __call__(self):
        # set output as default to false
        output = False

        # make sure result is not set
        environment.set_env_value(self.__result_attribute, None)

        # run function
        res = self.__f()

        # if end of window reached we should
        # 1. reset state
        # 2. set start and end times
        # 3. set output to true
        # and set start and end times
        # we reach end of window when we have done something (call count is not zero)
        # and we we have run for size times
        if self.__call_count != 0 and self.__call_count % self.__size == self.__size - 1:
            environment.set_env_value(self.__result_attribute, res)
            environment.set_env_value(self.__start_attribute,
                                  self.__call_count - (self.__size-1))
            environment.set_env_value(self.__end_attribute,
                                  self.__call_count)
            # reset state
            self.__state = {}
            output = True

        self.__call_count += 1
        return output
