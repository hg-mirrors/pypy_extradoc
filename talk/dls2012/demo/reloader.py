import os, sys, time, traceback

class ReloadHack(object):
    def __init__(self, iterator_class):
        self.module = sys.modules[iterator_class.__module__]
        self.filename = self.module.__file__
        if self.filename.endswith('.pyc'):
            self.filename = self.filename[:-1]
        self.name = iterator_class.__name__
        self.mtime = -1
        self.iterator_class = iterator_class

    def __call__(self, *args, **kwargs):
        def wrapper():
            while True:
                while True:
                    try:
                        mtime = os.stat(self.filename).st_mtime
                    except OSError:
                        pass
                    else:
                        try:
                            if mtime > self.mtime:
                                self.mtime = mtime
                                reload(self.module)
                                self.iterator_class = getattr(self.module, self.name).iterator_class
                                obj = iter(self.iterator_class(*args, **kwargs))
                                halted = False
                        except Exception as e:
                            print
                            traceback.print_exc()
                        else:
                            if not halted:
                                break
                try:
                    yield obj.next()
                except Exception as e:
                    print
                    traceback.print_exc()
                    halted = True


        return wrapper()

