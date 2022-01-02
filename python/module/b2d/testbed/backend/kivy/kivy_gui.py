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
from kivy.uix.scatter import Scatter, ScatterPlane
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window

from dataclasses import dataclass, field

from ..gui_base import GuiBase


class KivyWidget(ScatterPlane):
    def __init__(self, kivy_gui, **kwargs):
        self.kivy_gui = kivy_gui
        super(KivyWidget, self).__init__(do_rotation=False)

        # dirty hack to resize window
        # Window.size = self.kivy_gui.resolution

        # clock to trigger stepping of world and rendering
        Clock.schedule_interval(self.step, self.kivy_gui._dt)

        # apply initial scale
        scale = self.kivy_gui.settings.scale
        self.apply_transform(Matrix().scale(scale, scale, scale), anchor=(0, 0))

        # keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def step(self, dt):
        self.canvas.clear()
        self.kivy_gui._testworld.step(dt)

        with self.canvas:
            self.kivy_gui._testworld.draw_debug_data()

    def handle_scroll(self, touch):
        factor = None
        if touch.button == "scrolldown":
            if self.scale < self.scale_max:
                factor = 1.1
        elif touch.button == "scrollup":
            if self.scale > self.scale_min:
                factor = 1 / 1.1
        if factor is not None:
            self.apply_transform(
                Matrix().scale(factor, factor, factor), anchor=touch.pos
            )

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.kivy_gui._testworld.on_keyboard_down(keycode[1])

    def on_keyboard_up(self, keyboard, keycode):
        self.kivy_gui._testworld.on_keyboard_up(keycode[1])

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
class KivyGui(App, GuiBase):
    def __init__(self, testbed_cls, settings, testbed_settings=None):

        super(KivyGui, self).__init__()

        self.settings = settings
        self.testbed_cls = testbed_cls
        self.testbed_settings = testbed_settings
        self._testworld = None

        self._fps = settings.fps
        self._dt = 1.0 / self._fps
        # self._t = settings.get('t',10)
        # self._n = int(0.5 + self._t / self._dt)

        # settings

        Config.set("graphics", "width", f"{settings.resolution[0]}")
        Config.set("graphics", "height", f"{settings.resolution[1]}")
        self.kivy_widget = KivyWidget(kivy_gui=self)
        self.debug_draw = KivyBatchDebugDraw(scatter=self.kivy_widget)

        self.debug_draw.screen_size = self.settings.resolution

    #
    def start_ui(self):
        self._testworld = self.testbed_cls(settings=self.testbed_settings)
        self._testworld.set_debug_draw(self.debug_draw)

        # start the kivy ui
        self.run()

    def build(self):
        return self.kivy_widget
