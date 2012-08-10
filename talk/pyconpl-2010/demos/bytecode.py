
def f(a, b):
    while a < b:
        a += 1
    return b

import dis
dis.dis(f)
