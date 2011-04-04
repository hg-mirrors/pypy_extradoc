
def call(d=None):
    if d is not None:
        return d
    return 1

def rare_case(i):
    return i % 100 == 0

def f():
    i = 0
    while i < 1000000:
        if rare_case(i):
            i += call(**{'d': 3})
        else:
            i += call()

f()
