import PyQt5
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore,QtWidgets
import pybox2d
import logging

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from . tools import *
from . debug_draw_view_box import *
# from . debug_draw import *
from . recording_renderer import *


class PlayPauseStopParameterItem(ParameterItem):
    def __init__(self, param, depth):
        ParameterItem.__init__(self, param, depth)
        self.layoutWidget = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget.setLayout(self.layout)

        self.is_paused = False
        self.style = self.layoutWidget.style()

        self.button_play_pause = QtGui.QToolButton()
        self.button_play_pause.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_MediaPause))
        self.button_step =       QtGui.QToolButton()
        self.button_step.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_ArrowRight))
        self.button_stop =       QtGui.QToolButton()
        self.button_stop.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_MediaStop))
        #self.layout.addSpacing(100)
        self.layout.addWidget(self.button_play_pause)
        self.layout.addWidget(self.button_step)
        self.layout.addWidget(self.button_stop)
        self.layout.addStretch()
        self.button_play_pause.clicked.connect(self.buttonPlayPauseClicked)
        self.button_step.clicked.connect(self.buttonStepClicked)
        self.button_stop.clicked.connect(self.buttonStopClicked)
        param.sigNameChanged.connect(self.paramRenamed)
        self.setText(0, '')
        
    def treeWidgetChanged(self):
        ParameterItem.treeWidgetChanged(self)
        tree = self.treeWidget()
        if tree is None:
            return
        
        tree.setFirstItemColumnSpanned(self, True)
        tree.setItemWidget(self, 0, self.layoutWidget)
        
    def paramRenamed(self, param, name):
        pass
        #self.button.setText(name)
        
    def buttonPlayPauseClicked(self):
        if self.is_paused:
            self.button_play_pause.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.button_play_pause.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.is_paused = not self.is_paused
        self.param.buttonPlayPauseClicked()
    def buttonStepClicked(self):
        self.is_paused = True
        self.button_play_pause.setIcon(self.style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.param.buttonStepClicked()
    def buttonStopClicked(self):
        self.param.buttonStopClicked()    
class PlayPauseStopParameter(Parameter):
    """Used for displaying a button within the tree."""
    itemClass = PlayPauseStopParameterItem
    sigPlayPauseClicked = QtCore.Signal(object)
    sigStepClicked = QtCore.Signal(object)
    sigStopClicked = QtCore.Signal(object)
    def buttonPlayPauseClicked(self):
        self.sigPlayPauseClicked.emit(self)
        self.emitStateChanged('playPauseClicked', None)
    def buttonStepClicked(self):
        self.sigStepClicked.emit(self)
        self.emitStateChanged('stepClicked', None)
    def buttonStopClicked(self):
        self.sigStopClicked.emit(self)
        self.emitStateChanged('stopClicked', None)
registerParameterType('play_pause_stop', PlayPauseStopParameter, override=True)



# this is what  framework sees/gets as gui
class PGGuiProxy(object):
    def __init__(self, parent, r=None, kd=None):
        self.renderer = r
        self._is_key_down = kd
        self._parent = parent
    def is_key_down(self, key):
        return self._is_key_down[key]


    def add_param(self, *args, **kwargs):
        return self._parent.add_param(*args, **kwargs)
    def get_param_value(self, *args, **kwargs):
        return self._parent.get_param_value(*args, **kwargs)


QT_KEY_MAP = {
    QtCore.Qt.Key_A : 'A',
    QtCore.Qt.Key_B : 'B',
    QtCore.Qt.Key_C : 'C',
    QtCore.Qt.Key_D : 'D',
    QtCore.Qt.Key_E : 'E',
    QtCore.Qt.Key_F : 'F',
    QtCore.Qt.Key_G : 'G',
    QtCore.Qt.Key_H : 'H',
    QtCore.Qt.Key_I : 'I',
    QtCore.Qt.Key_J : 'J',
    QtCore.Qt.Key_K : 'K',
    QtCore.Qt.Key_L : 'L',
    QtCore.Qt.Key_M : 'M',
    QtCore.Qt.Key_N : 'N',
    QtCore.Qt.Key_O : 'O',
    QtCore.Qt.Key_P : 'P',
    QtCore.Qt.Key_Q : 'Q',
    QtCore.Qt.Key_R : 'R',
    QtCore.Qt.Key_S : 'S',
    QtCore.Qt.Key_T : 'T',
    QtCore.Qt.Key_U : 'U',
    QtCore.Qt.Key_V : 'V',
    QtCore.Qt.Key_W : 'W',
    QtCore.Qt.Key_X : 'X',
    QtCore.Qt.Key_Y : 'Y',
    QtCore.Qt.Key_Z : 'Z',
    QtCore.Qt.Key_0 : '0',
    QtCore.Qt.Key_1 : '1',
    QtCore.Qt.Key_2 : '2',
    QtCore.Qt.Key_3 : '3',
    QtCore.Qt.Key_4 : '4',
    QtCore.Qt.Key_5 : '5',
    QtCore.Qt.Key_6 : '6',
    QtCore.Qt.Key_7 : '7',
    QtCore.Qt.Key_8 : '8',
    QtCore.Qt.Key_9 : '9',
    QtCore.Qt.Key_Space : ' '
}

class PgFrameworkWidget(QtGui.QWidget):

    def __init__(self, testbed, parent=None):
        super(PgFrameworkWidget, self).__init__(parent)

        self.gui = PGGuiProxy(parent=self)

        self.init_ui()
        self.init_parameter_tree()
        self.init_timer()
        self.init_key_handling()
        
        self.target_fps = 60.0
        self.testbed = testbed
        self.is_paused = True
        self.dt = 1.0 / self.target_fps
        
        


        self.framework = self.construct_example()


        
        self.view_box.set_example(self.framework)

        # start
        self.start_playing()




    def init_key_handling(self):
        # currently pressed keys
        self._is_key_down = dict()
        for key in QT_KEY_MAP.keys():
            self._is_key_down[QT_KEY_MAP[key]] = False
        self.gui._is_key_down = self._is_key_down

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key in QT_KEY_MAP:
            str_key = QT_KEY_MAP[key]
            self._is_key_down[str_key] = True

            if  self.framework.on_key_down(str_key):
                event.accept()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key in QT_KEY_MAP:
            str_key = QT_KEY_MAP[key]
            self._is_key_down[str_key] = False
            if  self.framework.on_key_up(str_key):
                event.accept()



    def init_timer(self):
        self.qtimer = QtCore.QTimer(self)
        self.qtimer.timeout.connect(self.step)

    def add_param(self, *args, **kwargs):
        # try to get exisiting
        p_new = Parameter.create(*args, **kwargs)
        try:
            p = self.example_param.child(p_new.name())
        except :
            self.example_param.addChild(p_new)
            p = p_new
        return p.value()


    def get_param_value(self, *args, **kwargs):
        p = self.example_param.param(*args, **kwargs)
        return self.example_param.param(*args, **kwargs).value()

    def init_parameter_tree(self):
        params = [
            {'name': 'PlaySettings', 'type': 'group', 'children': [
                {'name': 'play_pause_stop', 'type':  'play_pause_stop'},            
                ]},
        ]
        self.parameter = Parameter.create(name='params', type='group', children=params)
        self.parameter_tree.setParameters(self.parameter, showTop=False)
        self.play_param = self.parameter.param('PlaySettings')
        self.play_param.param('play_pause_stop').sigPlayPauseClicked.connect(self.toggle_start_pause_playing)
        self.play_param.param('play_pause_stop').sigStepClicked.connect(self.pause_and_play_single_step)
        self.play_param.param('play_pause_stop').sigStopClicked.connect(self.stop_playing)

        debug_draw_param = self.view_box.debug_draw_graphics_object.parameter
        self.parameter.addChild(debug_draw_param)

        self.example_param = Parameter.create(name='ExampleParam', type='group', children=[])
        self.parameter.addChild(self.example_param)

    def init_ui(self):

        self.hbox = QtGui.QHBoxLayout()
        self.setLayout(self.hbox)


        self.graphView = pg.GraphicsView()
        self.graphViewLayout = pg.GraphicsLayout()
        self.graphView.setCentralItem(self.graphViewLayout)
        self.view_box = DebugDrawViewBox() 
        # self.debug_draw_graphics_object = self.view_box.debug_draw_graphics_object
        # self.debug_draw_graphics_object.master = self
        self.gui.renderer = self.view_box.debug_draw_graphics_object.recording_renderer

        self.graphViewLayout.addItem(self.view_box)


        self.parameter_tree = ParameterTree()


        ## Title at top
        self.info_textitem = pg.TextItem("FPS: NONE")
        self.graphView.addItem(self.info_textitem)#,0,0)






        #self.graphViewLayout.addItem(self.info_textitem)
        #self.graphViewLayout.nextRow()

        

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.hbox.addWidget(self.splitter)

        self.splitter.addWidget(self.graphView)
        self.splitter.addWidget(self.parameter_tree)

    def reset_example(self):
        was_paused = bool(self.is_paused)
        self.pause_play()
        self.framework = self.construct_example()
        self.world = self.framework.world
        self.view_box.set_example(self.framework)
        
        if  was_paused:
            self.view_box.updateDebugDraw()
            self.start_playing()
            self.pause_play()
        else:
            self.view_box.updateDebugDraw()
            self.start_playing()

    def construct_example(self):
        
        framework = self.testbed.exampleCls(gui=self.gui)
        framework.gui = self.gui
        aa = framework.description
        self.info_textitem.setText(aa)
        return framework

    def toggle_start_pause_playing(self):
        if self.is_paused:
            self.start_playing()
        else:
            self.pause_play()

    def start_playing(self):
        self.view_box.update()
        if self.is_paused:
            self.qtimer.start((1.0/self.target_fps)*1000.0) #.5 seconds
            self.is_paused  = False

    def pause_and_play_single_step(self):
        self.pause_play()
        self.step()

    def stop_playing(self):
        self.reset_example()

    def pause_play(self):
        if self.is_paused:
            pass
        else:
            self.qtimer.stop() #.5 seconds
            self.is_paused = True
        
    def step(self):

        self.framework.pre_step(self.dt)
        self.framework.step(self.dt)
        self.framework.post_step(self.dt)

        self.view_box.updateDebugDraw()
        self.update_info_text()

    def update_info_text(self):



        current_fps = self.framework.current_fps 
        target_fps = self.target_fps
        info = self.framework.description

        text = """ 
            {info}
            FPS: {current_fps:.2f},{target_fps:.2f}
            
        """.format(info=info,current_fps=current_fps, target_fps=target_fps)
        self.info_textitem.setText(text)





class PgTestbedGui(object):
    def __init__(self, testbed):
        self.testbed = testbed
        

    def run(self):

        
        app = QtGui.QApplication([])
        vbw = PgFrameworkWidget(testbed=self.testbed)
        vbw.show()
        QtGui.QApplication.instance().exec_()
