

class Box:
    pass

class IntBox(Box):
    def __init__(self, intval):
        self.intval = intval
    def as_int(self):
        return self.intval
    def as_str(self):
        return str(self.intval)

class StrBox(Box):
    def __init__(self, strval):
        self.strval = strval
    def as_int(self):
        return int(self.strval)
    def as_str(self):
        return self.strval


def func_add_int(ix, iy): return ix + iy
def func_sub_int(ix, iy): return ix - iy
def func_mul_int(ix, iy): return ix * iy

def func_add_str(sx, sy): return sx + ' ' + sy
def func_sub_str(sx, sy): return sx + '-' + sy
def func_mul_str(sx, sy): return sx + '*' + sy

def op2(stack, func_int, func_str):
    y = stack.pop()
    x = stack.pop()
    try:
        z = IntBox(func_int(x.as_int(), y.as_int()))
    except ValueError:
        z = StrBox(func_str(x.as_str(), y.as_str()))
    stack.append(z)


def interpret(bytecode, args):
    loops = []
    stack = []
    pos = 0
    while pos < len(bytecode):
        opcode = bytecode[pos]
        pos += 1
        if   opcode == 'ADD': op2(stack, func_add_int, func_add_str)
        elif opcode == 'SUB': op2(stack, func_sub_int, func_sub_str)
        elif opcode == 'MUL': op2(stack, func_mul_int, func_mul_str)
        elif opcode[0] == '#':
            n = int(opcode[1:])
            stack.append(args[n-1])
        elif opcode.startswith('->#'):
            n = int(opcode[3:])
            args[n-1] = stack.pop()
        elif opcode == '{':
            loops.append(pos)
        elif opcode == '}':
            if stack.pop().as_int() == 0:
                loops.pop()
            else:
                pos = loops[-1]
        else:
            stack.append(StrBox(opcode))
    while len(stack) > 1:
        op2(stack, func_add_int, func_add_str)
    return stack.pop()


def test_main():
    main = """#1 5 ADD""".split()
    res = interpret(main, [IntBox(20)])
    assert res.as_int() == 25
    res = interpret(main, [StrBox('foo')])
    assert res.as_str() == 'foo 5'

def test_factorial():
    factorial = """The factorial of #1 is
                      1 { #1 MUL #1 1 SUB ->#1 #1 }""".split()
    res = interpret(factorial, [IntBox(5)])
    assert res.as_str() == 'The factorial of 5 is 120'
