from pypy.rlib import jit
from pypy.jit.codewriter.policy import JitPolicy

class Base(object):
    def __init__(self, n):
        self.value = n

    @staticmethod
    def build(n):
        if n & 1 == 0:
            return Even(n)
        else:
            return Odd(n)

class Odd(Base):
    def f(self):
        return Even(self.value * 3 + 1)

class Even(Base):
    def f(self):
        n = self.value >> 2
        if n == 1:
            return None
        return self.build(n)

def main(args):
    i = 2
    if len(args) == 17:
        return -1
    while True:
        a = Base.build(i)
        j = 0
        while j < 100:
            j += 1
            myjitdriver.jit_merge_point(i=i, j=j, a=a)
            if a is None:
                break
            a = a.f()
        else:
            print i
        i += 1

def target(*args):
    return main, None

def jitpolicy(driver):
    """Returns the JIT policy to use when translating."""
    return JitPolicy()
myjitdriver = jit.JitDriver(greens=[], reds=['i', 'j', 'a'])

if __name__ == '__main__':
    import sys
    main(sys.argv)
