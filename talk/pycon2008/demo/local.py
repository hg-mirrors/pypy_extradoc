
from distributed import RemoteProtocol, remote_loop
from distributed.socklayer import Finished, socket_listener, socket_connecter
import sys
import pdb

PORT = 12122

def f():
    print "Calling f"
    return 8

def catch():
    try:
        r.get_remote('x').raising()
    except:
        import pdb
        pdb.post_mortem(sys.exc_info()[2])

if __name__ == '__main__':
    send, receive = socket_connecter(('localhost', PORT))
    r = RemoteProtocol(send, receive)
    import code
    code.interact(local=locals())
