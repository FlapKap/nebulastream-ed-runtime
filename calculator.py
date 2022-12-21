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
INT8 = const(1)
UINT8 = const(2)
INT16 = const(3)
UINT16 = const(4)
INT32 = const(5)
UINT32 = const(6)
INT64 = const(7)
UINT64 = const(8)
FLOAT = const(9)
DOUBLE = const(10)

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
    def __init__(self, program: bytes, stack_init=None, environment=None):
        # TODO: program as bytes limit values to 2^8. Should be fixed.
        self.program = program
        self.pc = 0  # program counter
        self.environment = environment if environment else []
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
            if inst in (CONST, VAR):
                instrs.append(str(next(instr_iter)))
        instrs = "[" + ",".join(instrs) + "]"
        return "Calculator(\n\tpc: {}\n\tprogram: {}\n\tenv: {}\n\t{})".format(self.pc, instrs, self.environment, self.s)

    def execute(self):
        while self.pc < len(self.program):
            instr = self.program[self.pc]
            self.pc += 1
            self.cases[instr]()

        return self.s.pop()

    def __pop_value(self):
        ## pop type of value
        typ = self.program[self.pc]
        self.pc += 1
        ## fetch value
        fmt = type_to_fmt[typ]
        value = struct.unpack_from(fmt, self.program, self.pc)[0]
        ## increment pc by length of value
        self.pc += struct.calcsize(fmt)
        
        return value

    def __const(self):
        '''push next element from program as data to the stack, and increase program counter'''
        self.s.push(self.__pop_value())
        self.pc += 1

    def __var(self):
        '''read next value from program as key to value in env, and push env value to stack'''
        var_index = self.program[struct.unpack_from("<B",self.program, self.pc)[0]]
        self.s.push(self.environment[var_index])
        self.pc += struct.calcsize("<B")

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
