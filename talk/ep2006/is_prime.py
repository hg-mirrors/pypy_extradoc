def find_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

def is_prime(n):
    divisors = find_divisors(n)
    return len(divisors) == 2



















class Expr(object):
    pass

class Value(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Plus(Expr):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def eval(self):
        return self.expr1.eval() + self.expr2.eval()

expr = Plus(Value(5), Plus(Value(30), Value(7)))

def example():
    return expr.eval()
