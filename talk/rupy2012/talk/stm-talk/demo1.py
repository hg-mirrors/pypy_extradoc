
class Number(object):

   def __init__(self, num):
       self.num = num

   def __add__(self, other):
       return Number(self.num + other.num)

   def __invert__(self):
       return Number(~self.num)

def foo(n):
    total = Number(0)
    for i in range(n):
        total += Number(i)
        total += ~ Number(i)
    return total.num

