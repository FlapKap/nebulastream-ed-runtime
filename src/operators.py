

class Operator:

    def __call__(self):
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
