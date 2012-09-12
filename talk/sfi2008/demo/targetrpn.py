import rpn

# __________  Entry point  __________

def entry_point(argv):
    code = argv[1]
    arg = int(argv[2])
    res = rpn.interpret(code, arg)
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point, None

