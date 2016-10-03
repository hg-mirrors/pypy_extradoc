
class X(object):
    def __init__(self, value):
        self.value = value

def make_list():
    lst = [X(5) for i in range(100)]
    lst.append(lst[50])
    return lst


lst = make_list()

for x in lst:
    x.value += 1

for i in range(len(lst)):
    x = lst[i]
    x.value += 1
    assert x.value == 7
