import b2d


class JupyterBatchDebugDraw(b2d.batch_debug_draw_cls(False, False, True)):
    def __init__(self, canvas, flags=None):
        super(JupyterBatchDebugDraw, self).__init__()

        # what is drawn
        if flags is None:
            flags = ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        self.flags = flags
        self.clear_flags(
            ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        )
        for flag in flags:
            self.append_flags(flag)

        # the canvas to draw on
        self._canvas = canvas

    def _draw_solid_polygons(self, points, sizes, colors):
        self._canvas.fill_styled_polygons(
            points=points.ravel(),
            points_per_polygon=sizes,
            color=colors.ravel(),
            alpha=1.0,
        )

    def _draw_polygons(self, points, sizes, colors):
        self._canvas.stroke_styled_polygons(
            points=points.ravel(),
            points_per_polygon=sizes,
            color=colors.ravel(),
            alpha=1.0,
        )

    def _draw_solid_circles(self, centers, radii, axis, colors):

        # ignore axis atm
        self._canvas.fill_styled_circles(
            centers[:, 0], centers[:, 1], radii, colors.ravel(), 1.0
        )

    def _draw_circles(self, centers, radii, colors):
        self._canvas.stroke_styled_circles(
            centers[:, 0], centers[:, 1], radii, color=colors.ravel(), alpha=1.0
        )

    def _draw_points(self, centers, sizes, colors):
        self._canvas.stroke_styled_circles(
            centers, sizes, color=colors.ravel(), alpha=1.0
        )

    def _draw_segments(self, points, colors):
        self._canvas.stroke_styled_line_segments(
            points=points, color=colors.ravel(), alpha=1.0
        )

    def _draw_particles(self, centers, radius, colors=None):

        radius = max(1, radius)
        if colors is None:

            # print("draw_particles",centers.shape, radius)
            r = radius
            self._canvas.save()
            self._canvas.translate(x=-r, y=-r)
            self._canvas.fill_style = "rgba(255,255,255,1)"
            self._canvas.fill_rects(centers[:, 0], centers[:, 1], r * 2)
            self._canvas.restore()

        else:
            alpha = (colors[:, 3]) / 255.0
            colors = colors[:, 0:3]

            r = radius
            self._canvas.save()
            self._canvas.translate(x=-r, y=-r)
            self._canvas.fill_styled_rects(
                centers[:, 0], centers[:, 1], r * 2, r * 2, colors, alpha
            )
            self._canvas.restore()

    def _uint8_color(self, color):
        return [c * 255 for c in color]

    def _line_width(self, line_width):
        screen_line_width = int(self.world_to_screen_scale(line_width) + 0.5)
        return max(1, screen_line_width)

    def _style(self, color):
        if len(color) == 3:
            return f"rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)})"
        elif len(color) == 4:
            return f"rgba({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)}, {int(color[3])})"

    # non-batch api
    def draw_solid_circle(self, center, radius, axis, color):
        screen_center = self.world_to_screen(center)
        screen_radius = self.world_to_screen_scale(radius)

        self._canvas.save()
        self._canvas.fill_style = self._style(color)
        self._canvas.fill_circle(screen_center[0], screen_center[1], screen_radius)
        self._canvas.restore()

    def draw_circle(self, center, radius, color, line_width=1):
        screen_center = self.world_to_screen(center)
        screen_radius = self.world_to_screen_scale(radius)
        screen_line_width = self._line_width(line_width)

        self._canvas.save()
        self._canvas.stroke_style = self._style(color)
        self._canvas.line_width = screen_line_width
        self._canvas.stroke_circle(screen_center[0], screen_center[1], screen_radius)
        self._canvas.restore()

    def draw_segment(self, p1, p2, color, line_width=1):
        screen_p1 = self.world_to_screen(p1)
        screen_p2 = self.world_to_screen(p2)
        screen_line_width = self._line_width(line_width)

        self._canvas.save()
        self._canvas.stroke_style = self._style(color)
        self._canvas.line_width = screen_line_width
        self._canvas.stroke_line(screen_p1[0], screen_p1[1], screen_p2[0], screen_p2[1])
        self._canvas.restore()

    def draw_polygon(self, vertices, color, line_width=1):
        # todo add C++ function for this
        screen_vertices = [self.world_to_screen(v) for v in vertices]
        screen_line_width = self._line_width(line_width)

        self._canvas.save()
        self._canvas.stroke_style = self._style(color)
        self._canvas.line_width = screen_line_width
        self._canvas.stroke_polygon(screen_vertices)
        self._canvas.restore()

    def draw_solid_polygon(self, vertices, color):
        # todo add C++ function for this
        screen_vertices = [self.world_to_screen(v) for v in vertices]
        self._canvas.save()
        self._canvas.fill_style = self._style(color)
        self._canvas.fill_polygon(screen_vertices)
        self._canvas.restore()
