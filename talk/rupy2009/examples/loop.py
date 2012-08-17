def f():
    i = 0
    s = 0
    while i < 10000000:
        s += (i % 10)
        i += 1

f()
