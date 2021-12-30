import numpy as np
from time import sleep
from threading import Event, Thread, Lock
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Label, HTML, Button, HBox, VBox
from ipyevents import Event as IPyEvent

import functools
import IPython
import time
from ipycanvas import Canvas, MultiCanvas, hold_canvas
import ipywidgets

from .jupyter_batch_debug_draw import JupyterBatchDebugDraw
from ..gui_base import GuiBase


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def scale_color(color):
    return [float(c) / 255.0 for c in color]


def rgb(color):
    r = int(color[0])
    g = int(color[1])
    b = int(color[2])
    return f"rgb({r},{g},{b})"


_id_to_gui = dict()


class JupyterGui(GuiBase):
    class Settings(GuiBase.Settings):
        id: object = None

    def __init__(self, testbed_cls, settings, testbed_settings=None):

        self.id = settings.id
        if settings.id is None:
            settings.id = testbed_cls

        if settings.id in _id_to_gui:
            old_self = _id_to_gui[settings.id]
            old_self._terminate()
        _id_to_gui[settings.id] = self

        self.settings = settings
        self.resolution = self.settings.resolution

        # steping settings
        self._fps = settings.fps
        self._dt_s = 1.0 / self._fps

        # testworld
        if testbed_settings is None:
            testbed_settings = dict()
        self.testbed_settings = testbed_settings
        self.testbed_cls = testbed_cls
        self.testbed = None

        # debug_draw
        self.debug_draw = None
        self.flip_bit = False

        # todo!
        self._debug_draw_flags = self.settings.get_debug_draw_flags()

        # flag to stop loop
        self._exit = False

        self.scale = settings.scale
        self.translate = settings.translate

        # Thread related
        # events
        self.paused = Event()
        self.reached_end = Event()
        self.world_lock = Lock()

        self._last_screen_pos = None
        self._mouse_is_down = False

    def _terminate(self):
        if not self.paused.isSet():
            self.paused.set()

    def make_testbed(self):

        if self.testbed is not None:
            self.testbed.say_goodbye_world()
        self.testbed = self.testbed_cls(settings=self.testbed_settings)

        # make debug draw
        self.debug_draw = JupyterBatchDebugDraw(
            self.multi_canvas[self.flip_bit], flags=self._debug_draw_flags
        )
        self.debug_draw.screen_size = self.resolution
        self.debug_draw.scale = self.scale
        self.debug_draw.translate = self.translate
        self.debug_draw.flip_y = True
        self.testbed.set_debug_draw(self.debug_draw)

    def start_ui(self):
        # make the canvas
        self.multi_canvas = MultiCanvas(
            n_canvases=2, width=self.resolution[0], height=self.resolution[1]
        )
        self.out = ipywidgets.Output()
        self.flip_bit = False

        # _setup_ipywidgets_gui
        self._setup_ipywidgets_gui()

        # make the world
        self.make_testbed()

        def on_mouse_down(xpos, ypos):
            if not self.paused.isSet():
                self._mouse_is_down = True
                self._last_screen_pos = xpos, ypos
                pos = self.debug_draw.screen_to_world(self._last_screen_pos)
                pos = pos.x, pos.y
                with self.world_lock:
                    self.testbed.on_mouse_down(pos)

        # moue callbacks
        def on_mouse_up(xpos, ypos):
            if not self.paused.isSet():
                self._mouse_is_down = False
                self._last_screen_pos = xpos, ypos
                pos = self.debug_draw.screen_to_world((xpos, ypos))
                pos = pos.x, pos.y
                with self.world_lock:
                    self.testbed.on_mouse_up(pos)

        def on_mouse_move(xpos, ypos):
            if not self.paused.isSet():
                lxpos, lypos = self._last_screen_pos
                self._last_screen_pos = xpos, ypos

                pos = self.debug_draw.screen_to_world((xpos, ypos))
                pos = pos.x, pos.y
                with self.world_lock:
                    handled_event = self.testbed.on_mouse_move(pos)
                    if (
                        not handled_event
                        and self._mouse_is_down
                        and self._last_screen_pos is not None
                    ):
                        dx, dy = xpos - lxpos, ypos - lypos

                        translate = self.debug_draw.translate
                        self.debug_draw.translate = (
                            translate[0] + dx,
                            translate[1] - dy,
                        )

        self.multi_canvas[1].on_mouse_down(on_mouse_down)
        self.multi_canvas[1].on_mouse_up(on_mouse_up)
        self.multi_canvas[1].on_mouse_move(on_mouse_move)

        d = IPyEvent(
            source=self.multi_canvas, watched_events=["keydown", "keyup", "wheel"]
        )

        def handle_event(event):

            scale = self.debug_draw.scale
            etype = event["event"]
            if etype == "wheel":
                if event["deltaY"] > 0:
                    self.debug_draw.scale = scale * 0.9
                elif event["deltaY"] < 0:
                    self.debug_draw.scale = scale * 1.1
                # self.event_info.value = f"WHEEEL {event['deltaY']}"
            elif etype == "keyup":
                k = event["key"]
                self.testbed.on_keyboard_up(k)
            elif etype == "keydown":
                k = event["key"]
                self.testbed.on_keyboard_down(k)

        d.on_dom_event(handle_event)

        for ci in range(2):
            self.multi_canvas[ci].line_width = 1

        Thread(target=self._loop).start()  # Start it by default

        return self

    def _loop(self):
        if self.reached_end.isSet():
            self.reached_end.clear()
        # Event loop
        while not self.paused.isSet():

            t0 = time.time()
            if self._exit:
                break

            self._single_step()
            t1 = time.time()

            delta = t1 - t0
            if delta < self._dt_s:
                time.sleep(self._dt_s - delta)
        self.reached_end.set()

    def _setup_ipywidgets_gui(self):
        # buttons
        start_btn = Button(icon="play")
        step_forward_btn = Button(icon="step-forward")
        step_forward_btn.disabled = True
        pause_btn = Button(icon="pause")
        reset_btn = Button(icon="stop")

        zoom_in_btn = Button(icon="search-plus")
        zoom_out_btn = Button(icon="search-minus")

        # sliders speed / fps
        fps_slider = ipywidgets.IntSlider(value=self._fps, min=1, max=100, step=1)

        speed_slider = ipywidgets.FloatSlider(value=1.0, min=0.1, max=10.0, step=0.1)

        def pause(btn=None):
            if not self.paused.isSet():
                step_forward_btn.disabled = False
                self.paused.set()

        pause_btn.on_click(pause)

        def start(btn=None):
            step_forward_btn.disabled = True
            if self.paused.isSet():
                self.paused.clear()
            if self.reached_end.isSet():
                self.reached_end.clear()
                Thread(target=self._loop).start()

        start_btn.on_click(start)

        def step_forward(btn=None):
            self._single_step()

        step_forward_btn.on_click(step_forward)

        def reset(btn):
            pause()
            while not self.reached_end.wait(0.02):
                pass
            self.make_testbed()
            self._single_step()
            # start()

        reset_btn.on_click(reset)

        def zoom_in(btn=None):
            s = self.debug_draw.scale
            self.debug_draw.scale = s * 1.2

        zoom_in_btn.on_click(zoom_in)

        def zoom_out(btn=None):
            s = self.debug_draw.scale
            s /= 1.2
            s = max(1, s)
            self.debug_draw.scale = s

        zoom_out_btn.on_click(zoom_out)

        draw_checkboxes = dict(
            shapes=ipywidgets.Checkbox(value=True),
            joints=ipywidgets.Checkbox(value=True),
            aabb=ipywidgets.Checkbox(value=False),
            com=ipywidgets.Checkbox(value=False),
            pairs=ipywidgets.Checkbox(value=False),
        )

        def on_flag_change(v, flag):
            v = v["new"]
            if v:
                self.debug_draw.append_flags(flag)
            else:
                self.debug_draw.clear_flags([flag])

            if self.paused.isSet():
                self._draw_world(self.debug_draw._canvas)

        # play buttons
        play_buttons = HBox([start_btn, step_forward_btn, pause_btn, reset_btn])

        # zoom
        zoom_buttons = HBox([zoom_in_btn, zoom_out_btn])

        # debug draw flags
        items = []
        flags = ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        for f in flags:
            label = ipywidgets.Label(value=f"Draw {f} :")
            checkbox = ipywidgets.Checkbox(value=bool(f in self._debug_draw_flags))
            checkbox.observe(functools.partial(on_flag_change, flag=f), names="value")
            items.append(label)
            items.append(checkbox)
        draw_flags = ipywidgets.GridBox(
            items, layout=ipywidgets.Layout(grid_template_columns="repeat(4, 200px)")
        )

        # tab organizing everything
        children = [play_buttons, zoom_buttons, draw_flags]
        tab = ipywidgets.Tab()
        tab.children = children
        for i, t in enumerate(["Stepping", "Zoom", "DebugDrawFlags"]):
            tab.set_title(i, str(t))
        # display
        self.event_info = HTML("Event info")
        IPython.display.display(self.out)
        with self.out:
            IPython.display.display(self.multi_canvas, tab)
            # IPython.display.display(self.event_info)

    def _single_step(self):

        canvas = self.multi_canvas[self.flip_bit]
        self.flip_bit = not self.flip_bit
        next_canvas = self.multi_canvas[self.flip_bit]

        with hold_canvas(next_canvas):
            self.debug_draw._canvas = next_canvas

            old_style = next_canvas.fill_style
            next_canvas.fill_style = "black"
            next_canvas.fill_rect(0, 0, self.resolution[0], self.resolution[1])

            self._step_world()

            next_canvas.fill_style = old_style

        # clear this one
        canvas.clear()

    def _step_world(self):

        with self.world_lock:
            self.testbed.step(self._dt_s)
