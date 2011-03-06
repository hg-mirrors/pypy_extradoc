
def f():
    i = 0
    s = 0
    while i < 3000:
        if i % 3 == 0:
            s += 1
        else:
            s += 2
        i += 1
    return s

if __name__ == '__main__':
    f()
