import inspect
import math


class GenericB2dIter(object):
    def __init__(self, currentItem):
        self.currentItem = currentItem

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def next(self):
        if self.currentItem is None:
            raise StopIteration
        else:
            c = self.currentItem
            self.currentItem = c.next
            return c


def _classExtender(moreCls, methods, baseCls=None):
    if baseCls is None:
        baseCls = inspect.getmro(moreCls)[1]
    for m in methods:
        setattr(baseCls, m, moreCls.__dict__[m])
