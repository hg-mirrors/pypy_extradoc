
def adder(x, y):
    return x + y

def entry_point(argv):
    if len(argv) != 3:
        print "Wrong number of args"
        return 1
    try:
        arg0 = int(argv[1])
        arg1 = int(argv[2])
    except ValueError:
        print "Requires ints"
        return 1
    print "Added", arg0 + arg1
    return 0

def target(*args):
    return entry_point

if __name__ == '__main__':
    import sys
    entry_point(sys.argv)
