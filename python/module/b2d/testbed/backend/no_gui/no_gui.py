import b2d 
from dataclasses import dataclass,field
from ..gui_base import GuiBase

class EmptyDebugDraw(b2d.batch_debug_draw_cls(False, True, True)):

    def __init__(self):
        super(EmptyDebugDraw,self).__init__()


    def draw_solid_polygons(self, points, sizes, colors):
        pass

    def draw_polygons(self, points, sizes, colors):
        pass

    def draw_solid_circles(self, centers, radii, axis, colors):
        pass

    def draw_circles(self, centers, radii, colors):
        pass

    def _draw_circles(self, centers, radii,  colors, lw):
        pass

    def draw_points(self, centers, sizes, colors):
        pass

    def draw_segments(self, points, colors):
        pass

    def draw_particles(self, centers, radius, colors=None):
        pass


class NoGui(GuiBase):

    @dataclass
    class Settings(GuiBase.Settings):
        t: float = 10.0

    def __init__(self, testbed_cls, settings, testbed_settings):
        
        self.testbed_cls = testbed_cls
        self.testbed_settings = testbed_settings
        self._testworld = None

        fps = testbed_settings.fps
        self._dt =1.0 / fps
        self._t = settings.t
        self._n = int(0.5 + self._t / self._dt) 
        self.debug_draw = EmptyDebugDraw()
        

    # run the world for a limited amount of steps
    def start_ui(self):
        
        self._testworld = self.testbed_cls(**self.testbed_settings)
        self._testworld.set_debug_draw(self.debug_draw)

        for i in range(self._n):
            self._testworld.step(self._dt)
