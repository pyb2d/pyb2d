import pybox2d as b2





class JupyterBatchDebugDraw(b2.BatchDebugDrawNew):

    def __init__(self, canvas, flags=None):
        super(JupyterBatchDebugDraw,self).__init__()

        # what is drawn
        if flags is None:
            flags = ['shape','joint','aabb','pair','center_of_mass','particle']
        self.clear_flags(['shape','joint','aabb','pair','center_of_mass','particle'])
        for flag in flags:
            self.append_flags(flag)

        # the canvas to draw on
        self._canvas = canvas

    def draw_solid_polygons(self, points, sizes, colors):
        self._canvas.batch_fill_polygons(
            points=points.ravel(),
            sizes=sizes,
            color=colors.ravel(),
            alpha=1.0
        )

    def draw_polygons(self, points, sizes, colors):
        self._canvas.batch_stroke_polygons(
            points=points.ravel(),
            sizes=sizes,
            color=colors.ravel(),
            alpha=1.0
        )

    def draw_solid_circles(self, centers, radii, axis, colors):
        
        # ignore axis atm
        self._canvas.batch_fill_circles(
            centers,
            radii,
            colors.ravel(),
            1.0
        )
        
    def draw_circles(self, centers, radii, colors):
        self._canvas.batch_stroke_circles(
            centers,
            radii,
            color=colors.ravel(),
            alpha=1.0
        )

    def draw_points(self, centers, sizes, colors):
        self._canvas.batch_stroke_circles(
            centers,
            sizes,
            color=colors.ravel(),
            alpha=1.0
        )

    def draw_segments(self, points, colors):
        self._canvas.batch_stroke_line_segments(
            points=points,
            color=colors.ravel(),
            alpha=1.0,
            sizes=None
        )


    def draw_particles(self, centers, radius, colors):
        pass

