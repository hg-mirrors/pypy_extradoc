from time import clock
d = {}
t0 = clock()

class A(object):
    def __init__(self, previous):
        self.previous = previous

maxi = 100000
rounds = 10
for r in range(rounds):
    i = 0
    p = A(None)
    while i < maxi:
        p = A(p)
        i += 1
    print clock() - t0
    maxi *= 2
