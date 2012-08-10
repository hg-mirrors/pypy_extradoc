from pypy.rlib.jit import hint

# ____________________________________________________________

class State:

    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def add(self):
        y = self.stack.pop()
        x = self.stack.pop()
        self.stack.append(x + y)

    def getresult(self):
        return self.stack[-1]


def interpret(code, arg):
    state = State()
    state.push(arg)
    i = 0
    while i < len(code):
        c = code[i]
        i = i + 1
        c = hint(c, concrete=True)       #  hint for the JIT
        if '0' <= c <= '9':
            state.push(ord(c) - ord('0'))
        elif c == '+':
            state.add()
    return state.getresult()

# ____________________________________________________________

def test_run():
    assert interpret("2 4 + + 3 +", 100) == 109

def test_lltype():
    from pypy.translator.interactive import Translation
    t = Translation(interpret)
    t.annotate([str, int])
    t.viewcg()
    t.rtype(type_system="lltype")
    t.viewcg()
