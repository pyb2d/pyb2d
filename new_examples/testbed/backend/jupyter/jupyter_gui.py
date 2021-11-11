import numpy as np
from time import sleep
from threading import Event, Thread
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Label, HTML, Button, HBox

import IPython
import time
from ipycanvas import Canvas,MultiCanvas, hold_canvas
import ipywidgets
from . jupyter_batch_debug_draw import JupyterBatchDebugDraw


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def scale_color(color):
    return [float(c)/255.0 for c in color]

def rgb(color):
    r = int(color[0])
    g = int(color[1])
    b = int(color[2])
    return f"rgb({r},{g},{b})"


class JupyterGui(object):
    def __init__(self, testbed_cls, settings=None, testbed_kwargs=None):
        
        # settings
        resolution = settings.get("resolution", (640,480))
        if resolution is None:
            resolution = (640,480)
        self.resolution = resolution

        self.settings = settings
        # steping settings
        self._fps = settings.get("fps", 30) 
        self._dt_s = 1.0 / self._fps

        # testworld
        if testbed_kwargs is None:
            testbed_kwargs = dict()
        self.testbed_kwargs = testbed_kwargs
        self.testbed_cls = testbed_cls
        self._testworld  = None

        # debug_draw
        self.debug_draw = None
        self.flip_bit = False
        self._debug_draw_flags = settings.get("draw_flags", ['shape','joint','particle'])

        # flag to stop loop
        self._exit = False
       
        self.scale = settings.get("scale", 30) 
        self.translate = settings.get("translate", (0, self.resolution[1]))



        # events
        self.paused = Event()
        self.reached_end = Event()

    def make_testworld(self):

        if self._testworld is not None:
            self._testworld.say_goodbye_world()
        self._testworld = self.testbed_cls(**self.testbed_kwargs)

        # make debug draw
        self.debug_draw = JupyterBatchDebugDraw(self.multi_canvas[self.flip_bit], 
            flags=self._debug_draw_flags)
        self.debug_draw.scale = self.scale
        self.debug_draw.translate = self.translate
        self.debug_draw.flip_y = True
        self._testworld.world.set_debug_draw(self.debug_draw)

    def start_ui(self):
        # make the canvas
        self.multi_canvas = MultiCanvas(n_canvases = 2, 
        width=self.resolution[0], height=self.resolution[1])
        self.out = ipywidgets.Output()
        self.flip_bit = False

        # buttons
        start_btn = Button(description='Start')
        pause_btn = Button(description='Pause')
        reset_btn = Button(description='Reset')


        def pause(btn=None):
            if not self.paused.isSet():
                self.paused.set()
        pause_btn.on_click(pause)

        def start(btn=None):
            if self.paused.isSet():
                self.paused.clear()
            if self.reached_end.isSet():
                self.reached_end.clear()
                Thread(target=loop).start() 
        start_btn.on_click(start)

        def reset(btn):
            pause()
            while not self.reached_end.wait(0.02):
                pass
            self.make_testworld()
            start()
        reset_btn.on_click(reset)


        # display
        IPython.display.display(self.out)
        with self.out:
            IPython.display.display(self.multi_canvas, HBox([start_btn, pause_btn, reset_btn]))
  

        #make the world
        self.make_testworld()



    
        target_fps = 30
        dt_desired_ms = (1.0/target_fps)*1000.0
        dt_desired_s = dt_desired_ms/1000.0
        



        for ci in range(2):
            self.multi_canvas[ci].line_width = self.settings.get("line_width", 1)
            # self.multi_canvas[ci].scale(self.scale, -1.0*self.scale)
            # self.multi_canvas[ci].line_width = 1.0 / self.scale


        def loop():
            if self.reached_end.isSet():
                self.reached_end.clear()
            # Event loop
            while not self.paused.isSet():
                
                t0 = time.time()
                if self._exit:
                    break

                self._step_world()

                canvas = self.multi_canvas[self.flip_bit]
                self.flip_bit = not self.flip_bit
                next_canvas = self.multi_canvas[self.flip_bit]
                assert canvas != next_canvas
                with hold_canvas(next_canvas):
                    self.debug_draw._canvas = next_canvas
                    self._draw_world(next_canvas)

                # clear this one
                canvas.clear()

                t1 = time.time()

                delta = t1 - t0
                if delta < self._dt_s:
                    time.sleep(self._dt_s - delta)
            self.reached_end.set()


        Thread(target=loop).start() # Start it by default


                

    def _step_world(self):
        self._testworld.step(self._dt_s)

    def _draw_world(self, canvas):
        old_style = canvas.fill_style
        canvas.fill_style = 'black'
        # canvas.fill_rect(0,0, self.resolution[0],self.resolution[1])

        self._testworld.world.draw_debug_data()
        # todo, cleapup this interface
        self.debug_draw.trigger_callbacks()
        self.debug_draw.reset()

        canvas.fill_style = old_style