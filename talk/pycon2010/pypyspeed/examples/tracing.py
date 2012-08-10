
def f():
    k = 0
    i = 0
    while i < 10000000:
        if k:
            i += 2
        i += 1

f()
