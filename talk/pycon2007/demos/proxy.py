from pypymagic import transparent_proxy
import urllib

class ControllerBase(object):
    def perform(self, name, *args, **kw):
        if name.startswith('__') and name.endswith('__'):
            attr = 'special_' + name[2:-2]
        else:
            attr = 'meth_' + name
        return getattr(self, attr)(*args, **kw)

class ListControllerBase(ControllerBase):
    """ implementation of list behaviour in terms of just 'getitem',
    'setitem' and 'insert'. """

    def getitem(self, item):
        raise NotImplementedError

    def setitem(self, item, value):
        raise NotImplementedError

    def delitem(self, item):
        raise NotImplementedError

    def insert(self, item, value):
        raise NotImplementedError

    def len(self):
        """ you probably want to override this too """
        return len(list(self._iter()))

    # ----------------------------------------------------------------

    def special_getitem(self, item):
        if isinstance(item, slice):
            return [self.getitem(i) for i in range(*item.indices(self.len()))]
        else:
            return self.getitem(item)

    def special_setitem(self, item, value):
        self.setitem(item, value)

    def special_delitem(self, item):
        self.delitem(item)

    def special_len(self):
        return self.len()

    def special_repr(self):
        r = []
        for i in range(len(self.proxy)):
            r.append(repr(self.proxy[i]))
        return '[' + ', '.join(r) + ']'

    def special_contains(self, obj):
        for o in self._iter():
            if o == obj:
                return True
        return False

    def meth_insert(self, item, value):
        self.insert(item, value)

    def _iter(self):
        i = 0
        while 1:
            try:
                yield self.getitem(i)
            except IndexError:
                return
            i += 1

class SillyListController(ListControllerBase):
    def getitem(self, item):
        if item > 9:
            raise IndexError
        else:
            return int(urllib.urlopen("http://localhost:8080/getitem?item=" + str(item)).read())

    def setitem(self, item, value):
        if item > 9:
            raise IndexError
        else:
            data = urllib.urlencode({'item':item, 'value':value})
            urllib.urlopen('http://localhost:8080/setitem', data=data).read()

def l():
    c = SillyListController()
    c.proxy = transparent_proxy(list, c.perform)
    return c.proxy

class InstanceController(object):
    pass

def wrap(cls, obj):
    controller = cls(obj)
    controller.proxy = transparent_proxy(type(obj), controller.perform)
    return controller.proxy

if __name__ == '__main__':
    print l()[0]
