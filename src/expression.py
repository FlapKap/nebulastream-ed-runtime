from micropython import const
import logging
import struct

logger = logging.getLogger(__name__)

# stack-based language
# consists of instr and values in a bytearray to execute operations on a stack
# there are 2 special operations: CONST and VAR.
# CONST: is followed by a type constant and a value of the size of the type constant.
# VAR: is followed by a uint8 value.
# it is assumed values from sensors are placed in the environement at an index corresponding to their id

# types
# maybe relevant if we want to represent the stack as a byte array for optimization purposes
# then we need to know the size of each type
INT8 = const(0)
UINT8 = const(1)
INT16 = const(2)
UINT16 = const(3)
INT32 = const(4)
UINT32 = const(5)
INT64 = const(6)
UINT64 = const(7)
FLOAT = const(8)
DOUBLE = const(9)

type_to_fmt = {
    INT8: "<b",
    UINT8: "<B",
    INT16: "<h",
    UINT16: "<H",
    INT32: "<i",
    UINT32: "<I",
    INT64: "<q",
    UINT64: "<Q",
    FLOAT: "<f",
    DOUBLE: "<d"
}
# instructions
# data
# these indicate that the next value in the instrlist is a value
CONST = const(0)
VAR = const(1)

# logical
AND = const(2)
OR = const(3)
NOT = const(4)

# relational
LT = const(5)
GT = const(6)
EQ = const(7)

# arithmetic
ADD = const(8)
SUB = const(9)
MUL = const(10)
DIV = const(11)
MOD = const(12)

instr_to_name = {
    CONST: "CONST",
    VAR: "VAR",
    AND: "AND",
    OR: "OR",
    NOT: "NOT",
    LT: "LT",
    GT: "GT",
    EQ: "EQ",
    ADD: "ADD",
    SUB: "SUB",
    MUL: "MUL",
    DIV: "DIV",
    MOD: "MOD"
}

type_to_name = {
    INT8: "INT8",
    UINT8: "UINT8",
    INT16: "INT16",
    UINT16: "UINT16",
    INT32: "INT32",
    UINT32: "UINT32",
    INT64: "INT64",
    UINT64: "UINT64",
    FLOAT: "FLOAT",
    DOUBLE: "DOUBLE"
}

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


def __debug(func):
    def decorated(self):
        before = str(self.stack)
        res = func(self)
        after = str(self.stack)
        logger.debug("{} called. Expression state\n{}".format(func, self))
        return res

    return decorated


class Expression:
    def __init__(self, program: bytes, stack=None, environment=None):
        self.program = program
        self.pc = 0  # program counter
        self.stack = stack if stack else Stack()
        self.environment = environment if environment else []
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

    def reset(self):
        self.pc = 0

    def __str__(self):
        # create list of instr as string
        instrs = []
        instr_iter = enumerate(self.program)
        pc = self.pc
        for i, inst in instr_iter:
            instr_str = instr_to_name[inst]
            if i == pc:  # if this is current instr, mark
                instr_str = "*{}*".format(instr_str)

            instrs.append(instr_str)

            # if current instr has data, append that data and advance iter
            # pretty annoyingly since we enumerate we have to fetch the second element
            if inst == VAR:
                instrs.append(str(next(instr_iter)[1]))
            elif inst == CONST:
                instrs.append(type_to_name[next(instr_iter)[1]])
                instrs.append(str(next(instr_iter)[1]))
        instrs = "[" + ",".join(instrs) + "]"
        return "Expression(\n\tpc: {}\n\tprogram: {}\n\tenv: {}\n\t{})".format(self.pc, instrs, self.environment, self.stack)

    def __call__(self, *args, **kwargs):
        logger.debug("Map called with: {} {}".format(args, kwargs))
        self.stack = kwargs["stack"] if "stack" in kwargs.keys() else Stack()
        self.pc = 0
        while self.pc < len(self.program):
            instr = self.program[self.pc]
            logger.debug("executing instr: {}\n{}".format(
                instr_to_name[instr], self))
            self.pc += 1
            self.cases[instr]()

        return self.stack.peek()

    def __pop_instr_value(self):
        # pop type of value
        typ = self.program[self.pc]
        self.pc += 1
        # fetch value
        fmt = type_to_fmt[typ]
        value = struct.unpack_from(fmt, self.program, self.pc)[0]
        # increment pc by length of value
        size = struct.calcsize(fmt)
        self.pc += size
        logger.debug("popped instr val: type: {}, fmt: {}, value: {}, size {}".format(
            type_to_name[typ], fmt, value, size))
        return value

    @__debug
    def __const(self):
        '''push next element from program as data to the stack, and increase program counter'''
        self.stack.push(self.__pop_instr_value())

    @__debug
    def __var(self):
        '''read next value from program as key to value in env, and push env value to stack'''
        var_index = self.program[struct.unpack_from(
            "<B", self.program, self.pc)[0]]
        self.stack.push(self.environment[var_index])
        self.pc += struct.calcsize("<B")

    @__debug
    def __and(self):
        self.stack.push(self.stack.pop() and self.stack.pop())

    @__debug
    def __or(self):
        self.stack.push(self.stack.pop() or self.stack.pop())

    @__debug
    def __not(self):
        self.stack.push(not self.stack.pop())

    @__debug
    def __lt(self):
        self.stack.push(self.stack.pop() < self.stack.pop())

    @__debug
    def __gt(self):
        self.stack.push(self.stack.pop() > self.stack.pop())

    @__debug
    def __eq(self):
        self.stack.push(self.stack.pop() == self.stack.pop())

    @__debug
    def __add(self):
        self.stack.push(self.stack.pop() + self.stack.pop())

    @__debug
    def __sub(self):
        self.stack.push(self.stack.pop() - self.stack.pop())

    @__debug
    def __mul(self):
        self.stack.push(self.stack.pop() * self.stack.pop())

    @__debug
    def __div(self):
        self.stack.push(self.stack.pop() / self.stack.pop())

    @__debug
    def __mod(self):
        self.stack.push(self.stack.pop() % self.stack.pop())