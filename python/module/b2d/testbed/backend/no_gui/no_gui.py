class EmptyDebugDraw(object):


    def begin_draw(self):
        pass

    def end_draw(self):
        pass

    def draw_solid_circle(self, center, radius, axis, c):
        pass 

    def draw_point(self, center, size, c):
        pass 

    def draw_circle(self, center, radius, c):
        pass 

    def draw_segment(self,v1, v2, c):
        pass 

    def draw_polygon(self,vertices, c):
        pass 

    def draw_solid_polygon(self,vertices, c):
        pass 

    def draw_particles(self, centers, radius,  c=None):
        pass 
    
    def draw_transform(self, xf):
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
