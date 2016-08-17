"""
This is a typical Functional Programming Languages demo, computing the
Fibonacci sequence by using an infinite lazy linked list.
"""

try:
    newvar    # only available in 'py.py -o logic'
except NameError:
    print __doc__
    raise SystemExit(2)

# ____________________________________________________________

Fibonacci = (1, (1, newvar()))

def generate():
    lst = Fibonacci
    while 1:
        (a, (b, tail)) = lst
        wait_needed(tail)
        newtail = newvar()
        unify(tail, (a+b, newtail))
        lst = lst[1]

def display(limit):
    cur = Fibonacci
    for i in range(limit):
        print cur[0]
        cur = cur[1]

uthread(generate)
uthread(display, 15)
