import os
if not hasattr(os, 'utime'):
    os.utime = lambda f:0
try:
    import stackless, types
    stackless.function = types.FunctionType
    stackless.instancemethod = types.MethodType
except ImportError:
    pass

from nevow import inevow, tags, loaders, rend, appserver
from twisted.application import internet, service
from twisted.internet import reactor
from zope.interface import implements
import random

import sys
sys.modules['syslog'] = internet

class GetItem(object):
    implements(inevow.IResource)
    def __init__(self, sharedlist):
        self.sharedlist = sharedlist
    def renderHTTP(self, ctx):
        item = int(ctx.arg('item'))
        req = ctx.locate(inevow.IRequest)
        req.setHeader('content-type', "text/plain")
        return str(self.sharedlist[item])

class SetItem(object):
    implements(inevow.IResource)
    def __init__(self, sharedlist):
        self.sharedlist = sharedlist
    def renderHTTP(self, ctx):
        item = int(ctx.arg('item'))
        value = int(ctx.arg('value'))
        self.sharedlist[item] = value
        req = ctx.locate(inevow.IRequest)
        req.redirect('/')
        return ''

class Root(rend.Page):
    def __init__(self, sharedlist):
        rend.Page.__init__(self)
        self.sharedlist = sharedlist
    docFactory = loaders.xmlstr('''\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "DTD/xhtml1-strict.dtd">
<html xmlns:nevow="http://nevow.com/ns/nevow/0.1">
 <head><title>A list</title></head>
 <body nevow:render="list">
  <nevow:slot name="list"/>
  <form action="getitem">
   Get Item: <input name="item" />
  </form>
  <form action="setitem" method="POST">
   Set Item: <input name="item" /> <input name="value" /> <input value="Submit" type="submit"/>
  </form>
 </body>
</html>
            ''')
    def render_list(self, ctx, data):
        return ctx.tag.fillSlots('list', str(self.sharedlist))

theList = range(10)
random.shuffle(theList)

application = service.Application("silly list server")

root = Root(theList)
root.putChild('getitem', GetItem(theList))
root.putChild('setitem', SetItem(theList))

internet.TCPServer(
    8080,
    appserver.NevowSite(
        root
    )
).setServiceParent(application)


