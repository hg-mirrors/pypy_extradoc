
class A(object):
    def __init__(self, value): 
        self.value = value

def f(n):
    print "running demo2..."
    i = A(0)
    while i.value < n:
        i = A(i.value + 1)
    return i
