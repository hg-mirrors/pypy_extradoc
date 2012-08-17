
class A(object):
    def __del__(self):
        pass

a = A()
print a.__del__.func_globals['a'] is a
