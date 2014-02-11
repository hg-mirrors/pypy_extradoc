

class Foo(object):

    def __init__(self, value):
        self.value = value

    def double(self):
        return Foo(self.value * 2)


def main(argv):
    if len(argv) <= 1:
        n = 22
    else:
        n = int(argv[1])

    lst = [Foo(i) for i in range(n)]

    print lst[-1].double().value
    return 0


# ____________________________________________________________

def target(*args):
    return main, None
