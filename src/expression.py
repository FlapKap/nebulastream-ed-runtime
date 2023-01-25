from micropython import const
import logging
import struct
import environment
import datatypes
logger = logging.getLogger(__name__)

# stack-based language
# consists of instr and values in a bytearray to execute operations on a stack
# there are 2 special operations: CONST and VAR.
# CONST: is followed by a type constant and a value of the size of the type constant.
# VAR: is followed by a uint8 value.
# it is assumed values from sensors are placed in the environement at an index corresponding to their id


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


def __debug(func):
    def decorated(self):
        #before = str(self.stack)
        res = func(self)
        #after = str(self.stack)
        logger.debug("{} called. Expression state\n{}".format(func, self))
        return res

    return decorated


class Expression:
    """
    Represents a stack-based programmed expression
    It works on a global stack with access to a global environment.
    Each instruction acts on the stack, or copies a value from the environment to the stack
    When the expression is called it is executed and the call returns the topmost element on the stack after execution
    it leaves the element on the stack

    TODO: contains a fair amount of code duplication that could be reduced
    """

    def __init__(self, program: bytes):
        self.program = program
        self.pc = 0  # program counter
        self.stack = environment.get_stack()
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

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Expression):
            return (
                self.program == __o.program and
                self.pc == __o.pc and
                self.stack == __o.stack
            )
        return False

    def __str__(self) -> str:
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
                value, size, typ, fmt = self.__read_instr_value(i)
                instrs.append(datatypes.type_to_name[typ])
                instrs.append(str(value))
                # advance iterator by type + size
                for i in range(0, size+1):
                    next(instr_iter)
        instrs = "[" + ",".join(instrs) + "]"
        return "Expression(pc={}\n\tprogram={},stack={})".format(self.pc, instrs, self.stack)

    def __call__(self, *args, **kwargs):
        logger.debug("Expression called")
        self.stack = kwargs["stack"] if "stack" in kwargs.keys() else environment.get_stack()

        # if called with arguments, we assume its input that needs to be pushed to the stack before operations start
        if args is not None:
            self.stack.push_multiple(args)

        self.pc = 0
        while self.pc < len(self.program):
            instr = self.program[self.pc]
            #logger.debug("executing instr: {}\n{}".format(instr_to_name[instr], self))
            self.pc += 1
            self.cases[instr]()

        return self.stack.peek()

    def __read_instr_value(self, i=None):
        # assume current pc is type
        index = i if i is not None else self.pc
        typ = self.program[index]
        fmt = datatypes.type_to_fmt[typ]
        size = struct.calcsize(fmt)
        value = struct.unpack_from(fmt, self.program, index + 1)[0]
        return value, size, typ, fmt

    def __pop_instr_value(self):
        # pop type of value
        value, size, typ, fmt = self.__read_instr_value()

        self.pc += size + 1
        logger.debug("popped instr val: type: {}, fmt: {}, value: {}, size {}".format(
            datatypes.type_to_name[typ], fmt, value, size))
        return value

    # @__debug
    def __const(self):
        '''push next element from program as data to the stack, and increase program counter'''
        self.stack.push(self.__pop_instr_value())

    # @__debug
    def __var(self):
        '''read next value from program as key to value in env, and push env value to stack'''
        var_index = struct.unpack_from(
            "<B", self.program, self.pc)[0]
        self.pc += 1
        self.stack.push(environment.get_env_value(var_index))

    @__debug
    def __and(self):
        # & doesn't short circuit
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 and l2)

    @__debug
    def __or(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 or l2)

    @__debug
    def __not(self):
        self.stack.push(not self.stack.pop())

    @__debug
    def __lt(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 < l2)

    @__debug
    def __gt(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 > l2)

    @__debug
    def __eq(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 == l2)

    @__debug
    def __add(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 + l2)

    @__debug
    def __sub(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 - l2)

    @__debug
    def __mul(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 * l2)

    @__debug
    def __div(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 / l2)

    @__debug
    def __mod(self):
        l2 = self.stack.pop()
        l1 = self.stack.pop()
        self.stack.push(l1 % l2)
