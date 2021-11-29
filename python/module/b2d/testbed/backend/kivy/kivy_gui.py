
from .kivy_debug_draw import *

# kivy-md
# from kivymd.app import MDApp
# from kivymd.uix.label import MDLabel
# from kivymd.app import MDApp

# kivy
from kivy.uix.widget import Widget
from kivy.graphics.instructions import *
from kivy.graphics.transformation import Matrix
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.config import Config
# from kivy.core.window import Window


class KivyWidget(Scatter):
    def __init__(self, kivy_gui, **kwargs):
        self.kivy_gui = kivy_gui
        super(KivyWidget, self).__init__(do_rotation=False)

        # dirty hack to resize window
        # Window.size = self.kivy_gui.resolution

        # clock to trigger stepping of world and rendering
        Clock.schedule_interval(self.step, self.kivy_gui._dt)


        # apply initial scale
        scale = self.kivy_gui.settings.get("scale", 30)
        self.apply_transform(Matrix().scale(scale, scale, scale),
                                     anchor=(0,0))

    def step(self, dt):
        self.canvas.clear()
        self.kivy_gui._testworld.step(dt)

        with self.canvas:
            self.kivy_gui._testworld.draw_debug_data()

    def handle_scroll(self, touch):
        factor = None
        if touch.button == 'scrolldown':
            if self.scale < self.scale_max:
                factor = 1.1
        elif touch.button == 'scrollup':
            if self.scale > self.scale_min:
                factor = 1 / 1.1
        if factor is not None:
            self.apply_transform(Matrix().scale(factor, factor, factor),
                                 anchor=touch.pos)
    def on_touch_down(self, touch):
        # Override Scatter's `on_touch_down` behavior for mouse scroll
        if touch.is_mouse_scrolling:
            self.handle_scroll(touch)
        else:
            world_pos = self.to_local(*touch.pos)
            handled_event = self.kivy_gui._testworld.on_mouse_down(world_pos)
            if not handled_event:
                super(KivyWidget, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.is_mouse_scrolling:
            pass
        else:
            world_pos = self.to_local(*touch.pos)
            handled_event = self.kivy_gui._testworld.on_mouse_up(world_pos)
            if not handled_event:
                super(KivyWidget, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        world_pos = self.to_local(*touch.pos)
        handled_event = self.kivy_gui._testworld.on_mouse_move(world_pos)
        if not handled_event:
            super(KivyWidget, self).on_touch_move(touch)

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


    # 
    def start_ui(self):
        self._testworld = self.testbed_cls(**self.testbed_kwargs)
        self._testworld.set_debug_draw(self.debug_draw)

        # start the kivy ui
        self.run()



    def build(self):
        return KivyWidget(kivy_gui=self)

