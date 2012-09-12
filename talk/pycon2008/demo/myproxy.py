import tputil
import urllib

class ProxyController(object):
    def __getitem__(self, item):
        data = urllib.urlencode({'item':item})
        return int(urllib.urlopen("http://localhost:8010/getitem?%s" % data,
                                   ).read())

    def __setitem__(self, item, value):
        data = urllib.urlencode({'item':item, 'value':value})
        urllib.urlopen("http://localhost:8010/setitem?%s" % data,
                       data=data).read()

    def __repr__(self):
        return urllib.urlopen("http://localhost:8010/").read()

def proxy_controller(oper):
    return oper.delegate()

l = tputil.make_proxy(proxy_controller, list, ProxyController())

import code
code.interact(local=locals())

