from subprocess import Popen, PIPE

from pypy.translator.js.lib import server
from pypy.translator.js.lib.support import js_source, callback
from pypy.translator.js.modules import dom

HTML = """<html><head>
<script src="stuff.js"></script>
</head><body onload="start()">
  <p id="s">Stuff</p>
</body></html>"""

def onupdate(msg):
    dom.document.getElementById("s").innerHTML = msg
    dom.setTimeout(start, 1000)

def start():
    exported_methods.update(onupdate)

class ExportedMethods(server.ExportedMethods):
    @callback(retval=str)
    def update(self):
        p = Popen('uptime', stdout=PIPE)
        p.wait()
        return p.stdout.read()

exported_methods = ExportedMethods()

class App(server.Collection):
    exported_methods = exported_methods
    def index(self):
        return HTML
    index.exposed = True

    def stuff_js(self):
        return "text/javascript", js_source([start])
    stuff_js.exposed = True

class Handler(server.NewHandler):
    application = App()

if __name__ == '__main__':
    httpd = server.create_server(handler=Handler, server_address=('', 7010))
    httpd.serve_forever()
