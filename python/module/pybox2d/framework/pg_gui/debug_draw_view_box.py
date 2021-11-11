import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore,QtWidgets


# from . tools import *
from . debug_draw import *
import pybox2d



class DebugDrawViewBox(pg.ViewBox):
    def __init__(self):
        super(DebugDrawViewBox, self).__init__(lockAspect=True,
                                        enableMouse=True)
        self.framework = None

        self.debug_draw_graphics_object = DebugDrawGraphicsObject()
        self.debug_draw = self.debug_draw_graphics_object.debug_draw
        self.addItem(self.debug_draw_graphics_object)

    def set_example(self, example):
        self.framework = example
        self.debug_draw_graphics_object.set_example(example)


    # def keyPressEvent(self, event):
    #     print('press the key: "%s" '%event.text())

    # def keyReleaseEvent(self, event):
    #     print('release the key: "%s" '%event.text())

    def mousePressEvent(self, ev):
        modifiers = QtGui.QApplication.keyboardModifiers()
        ctrl_mod = (modifiers == QtCore.Qt.ControlModifier)
        if ctrl_mod:
            super(DebugDrawViewBox, self).mousePressEvent(ev)
        else:
            debug_draw_graphics_object = self.debug_draw_graphics_object
            pos = ev.pos()
            canvas_pos = self.mapToView( pos)
            if self.framework.on_mouse_down(pybox2d.vec2(canvas_pos.x(),canvas_pos.y())):
                ev.accept()
            else:
                super(DebugDrawViewBox, self).mousePressEvent(ev)

      
    def mouseMoveEvent(self, ev):
        pos = ev.pos()
        canvas_pos = self.mapToView( pos)
        if self.framework.on_mouse_move(pybox2d.vec2(canvas_pos.x(),canvas_pos.y())):
            ev.accept()
        else:
            super(DebugDrawViewBox, self).mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        pos = ev.pos()
        canvas_pos = self.mapToView( pos)
        if self.framework.on_mouse_up(pybox2d.vec2(canvas_pos.x(),canvas_pos.y())):
            ev.accept()
        else:
            super(DebugDrawViewBox, self).mouseReleaseEvent(ev)


    def updateDebugDraw(self):
        
        self.debug_draw_graphics_object.update()
