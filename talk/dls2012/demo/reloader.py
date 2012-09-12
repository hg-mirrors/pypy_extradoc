import os, sys, time, traceback

class ReloadHack(object):
    def __new__(cls, *new_args, **new_kwargs):
        class Wrapper(object):
            module = sys.modules[cls.__module__]
            filename = module.__file__
            if filename.endswith('.pyc'):
                filename = filename[:-1]
            name = cls.__name__
            mtime = -1

            def update(self, *args, **kwargs):
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
                                    cls = getattr(self.module, self.name)
                                    self.obj = object.__new__(cls)
                                    self.obj.__init__(*new_args, **new_kwargs)
                                    self.halted = False
                            except Exception as e:
                                print
                                traceback.print_exc()
                            else:
                                if not self.halted:
                                    break
                    try:
                        return self.obj.update(*args, **kwargs)
                    except Exception as e:
                        print
                        traceback.print_exc()
                        self.halted = True

        return Wrapper()

def autoreload(fn):
    module = sys.modules[fn.__module__]
    filename = module.__file__
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    name = fn.__name__
    
    def wrapper(*args, **kwargs):
        halted = False
        while True:
            while True:
                try:
                    mtime = os.stat(filename).st_mtime
                except OSError:
                    pass
                else:
                    try:
                        if mtime > wrapper.last_mtime:
                            wrapper.last_mtime = mtime
                            reload(module)
                            wrapper.fn = getattr(module, name).fn
                            halted = False
                    except Exception as e:
                        print
                        traceback.print_exc()
                    else:
                        if not halted:
                            break
            try:
                return wrapper.fn(*args, **kwargs)
            except Exception as e:
                print
                traceback.print_exc()
                halted = True
    wrapper.fn = fn
    wrapper.last_mtime = -1

    return wrapper


