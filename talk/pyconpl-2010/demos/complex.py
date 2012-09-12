
class Number(object):
    def __init__(self, no):
        self.no = no
    
    def __add__(self, other):
        return Number(self.no + other.no)

def f():
    i = 0
    sum = Number(0)
    while i < 10000:
        sum = Number(1) + sum
        i += 1

f()
