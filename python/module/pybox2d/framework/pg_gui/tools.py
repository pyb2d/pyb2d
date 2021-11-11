import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy

the_dt = numpy.float64

def numpy_to_qpoly(vertices):
    n = vertices.shape[0]
    qpoints = QtGui.QPolygonF(n)
    vptr = qpoints.data()
    vptr.setsize(8*2*n)
    aa = numpy.ndarray( shape=(n,2), dtype='float64', buffer=vptr)
    aa.setflags(write=True)
    aa[:] = vertices
    return qpoints


class SaveRestore():
    def __init__(self, painter):
        self.painter = painter
    def __enter__(self):
        self.painter.save()
        return self.painter
    def __exit__(self, type, value, traceback):
        self.painter.restore()


