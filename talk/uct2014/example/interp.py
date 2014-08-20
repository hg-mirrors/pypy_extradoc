
import time

class InterpreterError(Exception):
    def __init__(self, msg):
        self.msg = msg

def interp(bytecode, start_value):
    i = 0
    lgt = len(bytecode)
    accumulator = start_value
    while i < lgt:
        c = bytecode[i]
        if c == 'd':
            accumulator -= 1
            i += 1
        elif c == 'l':
            arg = ord(bytecode[i + 1])
            i += 2
            if accumulator > 0:
                i -= arg + 2
        else:
            raise InterpreterError("Unknown char %s" % (c,))
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
