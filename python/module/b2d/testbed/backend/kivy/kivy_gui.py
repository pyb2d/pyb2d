try:
    from .kivy_debug_draw import *
except:
    from kivy_debug_draw import * 

# kivy-md
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

# kivy
from kivy.uix.widget import Widget
from kivy.graphics.instructions import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window


class KivyWidget(BoxLayout):
    def __init__(self, kivy_gui, **kwargs):
        self.kivy_gui = kivy_gui
        super(KivyWidget, self).__init__(**kwargs)

        Window.size = self.kivy_gui.resolution

        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.step, self.kivy_gui._dt)


        # with self.canvas:
        #     Color(0,1,0)
        #     Rectangle(size=self.size,pos=(100,0))

        # with self.canvas.before:
        #     # you can use this to add instructions rendered before
        #     pass
        # with self.canvas.after:
        #     # you can use this to add instructions rendered after
        #     pass
    def step(self, dt):
        self.canvas.clear()
        self.kivy_gui._testworld.step(dt)

        with self.canvas:
            self.kivy_gui._testworld.draw_debug_data()




# this class implements the "GUI" interface for b2d
class KivyGui(App):
    def __init__(self, testbed_cls, settings, testbed_kwargs=None):
        


        super(KivyGui, self).__init__()

        self.settings = settings
        self.testbed_cls = testbed_cls
        self.testbed_kwargs = testbed_kwargs
        self._testworld = None

        self._fps = settings.get('fps', 40.0)
        self._dt = 1.0 / self._fps
        self._t = settings.get('t',10)
        self._n = int(0.5 + self._t / self._dt)

        # settings
        resolution = settings.get("resolution",  (1000,1000))
        self.resolution = resolution

        Config.set('graphics', 'width', f'{resolution[0]}')
        Config.set('graphics', 'height', f'{resolution[1]}')



        self.image = numpy.zeros(list(self.resolution) + [3], dtype='uint8')
        self._image_list = []
        self.debug_draw = KivyBatchDebugDraw()

        self.debug_draw.screen_size = self.resolution
        self.debug_draw.flip_y = False
        self.debug_draw.scale = settings.get("scale", 20.0)
        self.debug_draw.translate = settings.get("translate", (10,10))



    # 
    def start_ui(self):
        self._testworld = self.testbed_cls(**self.testbed_kwargs)
        self._testworld.set_debug_draw(self.debug_draw)

        # start the kivy ui
        self.run()



    def build(self):

        l = BoxLayout()
        l.add_widget(KivyWidget(kivy_gui=self))
        return l

