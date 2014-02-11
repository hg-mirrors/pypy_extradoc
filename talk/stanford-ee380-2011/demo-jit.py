import sys
from pypy.rlib import jit


class Object:
    pass


class Integer(Object):

    def __init__(self, value):
        self.value = value

    def next(self):
        return Integer(self.value + 1)

    def small(self):
        return self.value < 1000000

    def as_str(self):
        return str(self.value)


class String(Object):

    def __init__(self, str):
        self.str = str

    def next(self):
        return String(self.str + "x")

    def small(self):
        return len(self.str) < 50

    def as_str(self):
        return self.str


jitdriver = jit.JitDriver(greens=['pc', 'bytecode'], reds=['input'])


def interpret(bytecode, input):
    pc = 0
    while True:
        jitdriver.jit_merge_point(bytecode=bytecode, input=input, pc=pc)

        nextop = bytecode[pc]
        pc += 1

        if nextop == 'n':
            input = input.next()

        elif nextop == 'l':
            if input.small():
                pc = 0
            else:
                return input.as_str()


# ____________________________________________________________


if __name__ == '__main__':
    print interpret("nl", String("x"))
    print interpret("nl", Integer(1))
    sys.exit()


# ____________________________________________________________


def main(argv):
    num = int(argv[2])
    print interpret(argv[1], Integer(num))
    return 0

def target(*args):
    return main, None


# ____________________________________________________________


from pypy.jit.codewriter.policy import JitPolicy

def jitpolicy(driver):
    return JitPolicy()
