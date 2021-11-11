import pybox2d

class ExtendedDebugDraw(pybox2d.DebugDraw):
    def __init__(self, float_colors=True):
        super(ExtendedDebugDraw, self).__init__(self, float_colors=float_colors)

    def draw_text(self, pos, text):
        raise NotImplementedError 

    def draw_point(self, pos):
        raise NotImplementedError 

    def draw_flat_polygon(self, vertices, color):
        raise NotImplementedError 
