from .opencv_debug_draw import *
import matplotlib.pyplot as plt
import imageio
import numpy
from ..gui_base import GuiBase
from typing import List, Optional


class GifGui(GuiBase):
    class Settings(GuiBase.Settings):
        filename: str = ""
        t: float = 10.0
        resolution: List[int] = [400, 400]
        scale: float = 10
        fps: int = 24  # we overwrite this here!
        t: float = 10.0

    def __init__(self, testbed_cls, settings, testbed_settings):

        self.settings = settings
        self.testbed_cls = testbed_cls
        self.testbed_settings = testbed_settings
        self._testworld = None

        self._fps = settings.fps
        self._dt = 1.0 / self._fps
        self._t = settings.t
        self._n = int(0.5 + self._t / self._dt)

        # settings

        self.image = numpy.zeros(list(self.settings.resolution) + [3], dtype="uint8")
        self._image_list = []
        self.debug_draw = OpenCvBatchDebugDraw(image=self.image)
        filename = self.settings.filename
        if filename == "":
            filename = f"{str(testbed_cls.__name__)}.gif"
        self._filename = filename
        self.debug_draw.screen_size = settings.resolution
        self.debug_draw.flip_y = True
        self.debug_draw.scale = settings.scale
        self.debug_draw.translate = settings.translate

    # run the world for a limited amount of steps
    def start_ui(self):

        self._testworld = self.testbed_cls(settings=self.testbed_settings)
        self._testworld.set_debug_draw(self.debug_draw)
        self._image_list = []

        for i in range(self._n):
            self._testworld.step(self._dt)
            self._testworld.draw_debug_data()

            self._image_list.append(self.image.copy())
            self.image[...] = 0

        imageio.mimsave(self._filename, self._image_list, fps=self._fps)
