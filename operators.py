

class Operator:

    def __call__(self):
        raise Exception("operator doesn't implement callable")


class Map(Operator):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        #TODO: move None handling (Result monad) outside
        return self.f(*args)

class Filter(Operator):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        def compute():
            if self.f(*args):
                if len(args) == 1:
                    return args[0]
                
                return args
            return None
            
        return compute()
