
def simple():
    for i in range(100000):
        pass









def bridge():
    s = 0
    for i in range(100000):
        if i % 2:
            s += 1
        else:
            s += 2







def bridge_overflow():
    s = 2
    for i in range(100000):
        s += i*i*i*i
    return s








def nested_loops():
    s = 0
    for i in range(10000):
        for j in range(100000):
            s += 1









def inner1():
    return 1

def inlined_call():
    s = 0
    for i in range(10000):
        s += inner1()









def inner2(a):
    for i in range(3):
        a += 1
    return a

def inlined_call_loop():
    s = 0
    for i in range(100000):
        s += inner2(i)






class A(object):
    def __init__(self, x):
        if x % 2:
            self.y = 3
        self.x = x

def object_maps():
    l = [A(i) for i in range(100)]
    s = 0
    for i in range(1000000):
        s += l[i % 100].x










if __name__ == '__main__':
    simple()
    bridge()
    bridge_overflow()
    nested_loops()
    inlined_call()
    inlined_call_loop()
    object_maps()
