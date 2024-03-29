import logging
logger = logging.getLogger(__name__)
# might be better in future to make class based on bytearray


class Stack:
    """
    A simple implementation of a stack. Supports the usual collection operators
    Iterates, and indexes, from oldest to newest.
    """

    def __init__(self, iterable=None):
        logger.debug("Initialise Stack with iterable {}".format(iterable))
        self.l = list(iterable) if iterable else []

    def __eq__(self, __o):
        if isinstance(__o, Stack):
            return self.l == __o.l
        return False

    def __len__(self):
        return len(self.l)

    def __iter__(self):
        yield from self.l

    def __str__(self):
        return "Stack: {}".format(self.l)

    def __repr__(self):
        return self.__str__()

    def peek(self, i=None):
        return self.l[i] if i else self.l[-1]

    def push(self, e):
        self.l.append(e)

    def push_multiple(self, it):
        self.l.extend(it)

    def pop(self):
        return self.l.pop()

    def pop_multiple(self, i):
        while i > 0:
            yield self.l.pop()
            i -= 1
