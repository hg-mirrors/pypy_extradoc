
class View(object):
    def __init__(self, arr, start, stop):
        self.arr = arr
        self.start = start
        self.stop = stop

    def __getitem__(self, item):
        if not isinstance(item, int):
            return NotImplemented
        if self.start + item <= self.stop:
            raise IndexError
        return self.arr[self.start + item]

class Wrapper(object):
    def __init__(self, arr):
        self.arr = arr

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.arr[item]
        elif isinstance(item, slice):
            if item.step != 1 or item.start < 0 or item.stop < 0:
                raise TypeError("step not implemented")
            return View(self.arr, item.start, item.stop)
        return NotImplemented
