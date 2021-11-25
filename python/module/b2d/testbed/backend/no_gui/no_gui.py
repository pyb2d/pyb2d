import b2d 

class EmptyDebugDraw(b2d.BatchDebugDrawNew):

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


class NoGui(object):
    def __init__(self, testbed_cls, settings, testbed_kwargs=None):
        
        self.testbed_cls = testbed_cls
        self.testbed_kwargs = testbed_kwargs
        self._testworld = None

        self._dt = settings.get('dt', 1.0/40.0)
        self._t = settings.get('t',10)
        self._n = int(0.5 + self._t / self._dt) 
        self.debug_draw = EmptyDebugDraw()
        

    # run the world for a limited amount of steps
    def start_ui(self):
        
        self._testworld = self.testbed_cls(**self.testbed_kwargs)
        self._testworld.set_debug_draw(self.debug_draw)

        for i in range(self._n):
            self._testworld.step(self._dt)
