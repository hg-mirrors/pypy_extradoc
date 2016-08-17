#!/usr/bin/env python
""" This is web server for slideshow which exports all the
necessary stuff for viewing pypy's presentation
"""

import py
from pypy.translator.js.lib import server

from pypy.rpython.ootypesystem.bltregistry import MethodDesc, BasicExternal,\
     described
from pypy.translator.js import commproxy
from pypy.translator.js.main import rpython2javascript
from pypy.translator.js.lib.support import callback

from pypy.translator.interactive import Translation

commproxy.USE_MOCHIKIT = True

FUNCTION_LIST = ['show', 'flow', 'annotate', 'rtype', 'const_fold', 'example']

class ExportedMethods(BasicExternal):
    _render_xmlhttp = True

    def _create_t(self):
        if hasattr(self, 't'):
            return
        def f(x):
            return 1

        def g(x):
            return f(x) + 3

        self.t = Translation(g)

    def _create_t2(self):
        if hasattr(self, 't2'):
            return
        def g():
            return 3
        
        def f():
            return g() + 1 * 2

        self.t2 = Translation(f)

    @callback(retval=None)
    def flow_basic(self):
        self._create_t()
        self.t.view()

    @callback(retval=None)
    def annotate_basic(self):
        self._create_t()
        self.t.annotate([int])
        self.t.view()

    @callback(retval=None)
    def rtype_basic(self):
        self._create_t()
        self.t.annotate([int])
        self.t.rtype()
        self.t.view()

    @callback(retval=None)
    def example(self):
        self._create_t2()
        self.t2.annotate()
        self.t2.rtype()
        self.t2.view()

    @callback(retval=None)
    def const_fold(self):
        self._create_t2()
        self.t2.backendopt()
        self.t2.view()

exported_methods = ExportedMethods()
main_path = py.path.local(__file__).dirpath()

class Handler(server.TestHandler):
    exported_methods = exported_methods

    def index(self):
        return main_path.dirpath().join("fireworks-slides.html").open().read()
    index.exposed = True

    def jssource_js(self):
        import slideshow
        javascript_source = rpython2javascript(slideshow,
                FUNCTION_LIST)
        return "text/javascript", javascript_source
    jssource_js.exposed = True

    def MochiKit_js(self):
        return "text/javascript", main_path.join("MochiKit.js").open().read()
    MochiKit_js.exposed = True

    def style_css(self):
        return "text/css", main_path.dirpath().join("style.css").open().read()
    style_css.exposed = True

if __name__ == '__main__':
    server.create_server(server_address=('localhost', 7071), handler=Handler).serve_forever()
