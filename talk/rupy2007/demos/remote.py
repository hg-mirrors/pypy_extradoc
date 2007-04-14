
from distributed import RemoteProtocol, remote_loop
from distributed.socklayer import Finished, socket_listener, socket_connecter
import sys

PORT = 12121

class X:
    def __init__(self):
        self.xxx = 3

    def meth(self, f):
        print "Calling meth"
        return f() + self.xxx

x = X()

if __name__ == '__main__':
    send, receive = socket_listener(address=('', PORT))
    try:
        remote_loop(RemoteProtocol(send, receive, globals()))
    except Finished:
        pass

