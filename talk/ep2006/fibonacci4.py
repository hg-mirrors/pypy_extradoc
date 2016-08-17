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

class Node:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

Fibonacci = Node(1, Node(1, newvar()))

def generate():
    lst = Fibonacci
    while 1:
        a = lst.head
        b = lst.tail.head
        wait_needed(lst.tail.tail)
        unify(lst, Node(a, Node(b, Node(a+b, newvar()))))
        lst = lst.tail

def display(limit):
    cur = Fibonacci
    for i in range(limit):
        print cur.head
        cur = cur.tail

uthread(generate)
uthread(display, 15)
