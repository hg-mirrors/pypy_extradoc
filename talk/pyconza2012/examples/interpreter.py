
(LOAD_FAST, LOAD_CONST, COMPARE_OP, POP_JUMP_IF_FALSE,
 ADD, STORE_FAST, JUMP_ABSOLUTE) = range(7)

has_arg = [True, True, False, True, False, True, True]

class BaseObject(object):
    def add(left, right):
        # try right
        return right.radd(left)

    def radd(self, left):
        raise TypeError

class Long(BaseObject):
    pass

class Integer(BaseObject):
    def __init__(self, v):
        self.intval = v
    
    def add(self, right):
        if isinstance(right, Integer):
            try:
                return Integer(self.intval + right.intval)
            except OverflowError:
                return Long(self.intval).add(Long(right.intval))
        else:
            return right.radd(self)

def interpret(bytecode, variables, constants):
    stack = []
    pos = 0
    arg0 = None
    while True:
        b = ord(bytecode[pos])
        if has_arg[b]:
            pos += 1
            arg0 = ord(bytecode[pos])
        if b == LOAD_FAST:
            stack.append(variables[arg0])
        elif b == LOAD_CONST:
            stack.append(constants[arg0])
        elif b == COMPARE_OP:
            right = stack.pop()
            left = stack.pop()
            stack.append(left.compare(right))
        elif b == ADD:
            right = stack.pop()
            left = stack.pop()
            stack.append(left.add(right))
        elif b == POP_JUMP_IF_FALSE:
            val = stack.pop()
            if not val.is_true():
                pos = arg0
                continue
        elif b == STORE_FAST:
            variables[arg0] = stack.pop()
        elif b == JUMP_ABSOLUTE:
            pos = arg0
            continue
        pos += 1


def f(a, b):
    return a + b

stack.append(variables[arg0])
stack.append(variables[arg0])
right = stack.pop()
left = stack.pop()
stack.append(left.add(right))
