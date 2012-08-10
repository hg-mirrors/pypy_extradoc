l = []
class A(object):
    def __del__(self):
        l.append(3)
A()
print l
