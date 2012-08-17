
def f():
    i = 0
    while i < 2000:
        i += 1
    print sys._getframe().f_locals
    # has to have 'i' as a local
    return i

if __name__ == '__main__':
    f()
