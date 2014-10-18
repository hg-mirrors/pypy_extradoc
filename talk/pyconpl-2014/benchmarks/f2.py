
def f():
    i = 0
    s = 0
    while i < 100000000:
        s += len(str(i))
        i += 1
    return s

print f()
