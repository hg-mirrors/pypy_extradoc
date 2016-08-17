
class A(object):
    def __init__(self, x):
        self.x = x

def f():
    a = A(1)
    i = 0
    while i < 2000:
        i += a.x

if __name__ == '__main__':
    f()
