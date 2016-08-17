
class A(object):
    def __init__(self, i, next):
        self.i = i
        self.next = next

def f():
    next = None
    for i in range(2000):
        next = A(i, next)
        
if __name__ == '__main__':
    f()
