
import time
from rpython.rlib import jit

driver = jit.JitDriver(greens = ['i', 'lgt', 'start_value', 'bytecode'],
                       reds = ['accumulator'])

class InterpreterError(Exception):
    def __init__(self, msg):
        self.msg = msg

def interp(bytecode, start_value):
    i = 0
    lgt = len(bytecode)
    accumulator = start_value
    while i < lgt:
        driver.jit_merge_point(bytecode=bytecode, i=i, lgt=lgt,
                               accumulator=accumulator, start_value=start_value)
        c = bytecode[i]
        if c == 'd':
            accumulator -= 1
            i += 1
        elif c == 'l':
            arg = ord(bytecode[i + 1])
            i += 2
            if accumulator > 0:
                i -= arg + 2
                driver.can_enter_jit(bytecode=bytecode, i=i, lgt=lgt,
                                     accumulator=accumulator,
                                     start_value=start_value)
        else:
            raise InterpreterError("Unknown char %s (%d)" % (c, ord(c)))
    return accumulator

def entry_point(argv):
    if len(argv) != 3:
        print "Wrong number of args, requires bytecode and start_value"
        return 1
    bytecode = argv[1]
    try:
        acc = int(argv[2])
    except ValueError:
        print "Expected int, got %s" % (argv[2],)
        return 2
    try:
        t0 = time.time()
        res = interp(bytecode, acc)
        tk = time.time()
        dt = tk - t0
    except InterpreterError, e:
        print e.msg
        return 3
    print "Got %d, time %f" % (res, dt)
    return 0

def target(*args):
    return entry_point

if __name__ == '__main__':
    import sys
    entry_point(sys.argv)
