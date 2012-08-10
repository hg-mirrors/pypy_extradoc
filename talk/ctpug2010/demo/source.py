
def g(i):
    return i + 1

def f():
    i = 0
    while i < 10000:
        i = g(i)

if __name__ == '__main__':
    f()
