import tiny

# __________  Entry point  __________

def entry_point(argv):
    if len(argv) < 2:
        print "usage: tiny 'program' args..."
        return 2
    program = argv[1]
    words = []
    i = 0
    while i < len(program):
        j = program.find(' ', i)
        if j < 0:
            j = len(program)
        if j > i:
            words.append(program[i:j])
        i = j + 1
    res = tiny.interpret(words, [tiny.StrBox(s) for s in argv[2:]])
    print res.as_str()
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point, None
