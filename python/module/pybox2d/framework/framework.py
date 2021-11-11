import pybox2d as b2d
from pybox2d import vec2
import time
import logging
# logging.warning('Watch out!')  # will print a message to the console
# logging.info('I told you so')  # will not print anything

from . framework_settings import *
from . framework_base     import *





class Framework(FrameworkBase):
    name = ""
    description = ""
    def __init__(self,gui,gravity=vec2(0,-9.81)):
        super(Framework, self).__init__(gui,gravity=gravity)

    



class Testbed(object):
    def __init__(self, guiType = "kivy", gui_kwargs = None):
        self.guiType =guiType
        if gui_kwargs is None:
            gui_kwargs = {}
        self.gui_kwargs = gui_kwargs
        if isinstance(guiType, str):
            if guiType == "kivy":
                from . framework_impl.kivy_gui import KivyTestbedGui
                self.guiCls = KivyTestbedGui
            elif guiType == "pygame":
                from . pygame_gui import PyGameTestbedGui
                self.guiCls = PyGameTestbedGui
            elif guiType == "pg":
                from . pg_gui import PgTestbedGui
                self.guiCls = PgTestbedGui
            elif guiType == "matplotlib":
                from . matplotlib import MatplotlibdGui
                self.guiCls = MatplotlibdGui
            else:
                raise RuntimeError("'%s' is an unknown gui cls")
        else:
            self.guiCls = guiType

    def setExample(self, cls):
        self.exampleCls = cls

    def run(self):
        self.guiCls(testbed=self, **self.gui_kwargs).run()
