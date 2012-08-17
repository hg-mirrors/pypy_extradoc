
def f():
    s = 0
    for i in xrange(100000000):
        s += 1
    return s

if __name__ == '__main__':
    import dis
    dis.dis(f)
    f()
