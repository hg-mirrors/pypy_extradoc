from pypy.translator.js.lib import server
from py.__.green.server.httpserver import GreenHTTPServer
import random

class Root(server.Collection):
    def __init__(self):
        self.l = range(10)
        random.shuffle(self.l)
    
    def index(self):
        return repr(self.l)
    index.exposed = True
    
    def getitem(self, item):
        return str(self.l[int(item)])
    getitem.exposed = True

    def setitem(self, item, value):
        self.l[int(item)] = int(value)
        return ""
    setitem.exposed = True

class Handler(server.NewHandler):
    application = Root()

if __name__ == '__main__':
    addr = ('', 8010)
    httpd = server.create_server(server_address=addr, handler=Handler,
                                 server=GreenHTTPServer)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    
