import sys
import pickle
import tputil

class X:
    def __init__(self, x):
        self.x = x
        self.caller = sys._getframe(1)

def proxy_controller(oper):
    result = oper.delegate()
    f = open("data", "w")
    f.write(pickle.dumps(oper.proxyobj))
    f.close() # explicit close
    return result

XXX # finish
