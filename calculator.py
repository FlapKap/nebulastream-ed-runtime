from micropython import const
from enum import IntEnum
import logging

logger = logging.getLogger(__name__)

# types
# maybe relevant if we want to represent the stack as a byte array for optimization purposes
# then we need to know the size of each type


# instructions
# data
# these indicate that the next value in the instrlist is a value
CONST = const(1)
VAR = const(2)

# logical
AND = const(3)
OR = const(4)
NOT = const(5)

# relational
LT = const(6)
GT = const(7)
EQ = const(8)

# arithmetic
ADD = const(9)
SUB = const(10)
MUL = const(11)
DIV = const(12)
MOD = const(13)


# might be better in future to make class based on bytearray
class Stack:
    def __init__(self, iterable=None):
        logger.debug("Initialise Stack with iterable {}".format(iterable))
        self.l = list(iterable) if iterable else []

    def __len__(self):
        return len(self.l)

    def __iter__(self):
        yield from self.l

    def __str__(self):
        return "Stack: {}".format(self.l)

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


class Calculator:
    def __init__(self, program: bytes, environment: list, stack_init=None):
        self.program = program
        self.pc = 0  # program counter
        self.environment = environment
        self.s = Stack(stack_init)
        self.cases = {
            CONST: self.__const,
            VAR: self.__var,
            AND: self.__and,
            OR: self.__or,
            NOT: self.__not,
            LT: self.__lt,
            GT: self.__gt,
            EQ: self.__eq,
            ADD: self.__add,
            SUB: self.__sub,
            MUL: self.__mul,
            DIV: self.__div,
            MOD: self.__mod
        }

    def execute(self):
        while self.pc < len(self.program):
            self.cases[self.program[self.pc]]()
            self.pc += 1
        

    def __const(self):
        '''push next element from program as data to the stack, and increase program counter'''
        self.s.push(self.program[self.pc])
        self.pc += 1

    def __var(self):
        '''read next value from program as key to value in env, and push env value to stack'''
        self.s.push(self.environment[self.program[self.pc]])
        self.pc += 1

    def __and(self):
        self.s.push(self.s.pop() and self.s.pop())

    def __or(self):
        self.s.push(self.s.pop() or self.s.pop())

    def __not(self):
        self.s.push(not self.s.pop())

    def __lt(self):
        self.s.push(self.s.pop() < self.s.pop())

    def __gt(self):
        self.s.push(self.s.pop() > self.s.pop())

    def __eq(self):
        self.s.push(self.s.pop() == self.s.pop())

    def __add(self):
        self.s.push(self.s.pop() + self.s.pop())

    def __sub(self):
        self.s.push(self.s.pop() - self.s.pop())

    def __mul(self):
        self.s.push(self.s.pop() * self.s.pop())
    
    def __div(self):
        self.s.push(self.s.pop() / self.s.pop())

    def __mod(self):
        self.s.push(self.s.pop() % self.s.pop())



