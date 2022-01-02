import numpy
import b2d
import pygame
import pygame.locals


class PyGameBatchDebugDraw(b2d.batch_debug_draw_cls(False, False, True)):
    def __init__(self, surface, flags=None):
        super(PyGameBatchDebugDraw, self).__init__()

        # what is drawn
        if flags is None:
            flags = ["shape", "joint"]  # ,'aabb','pair','center_of_mass','particle']
        self.flags = flags
        self.clear_flags(
            ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        )
        for flag in flags:
            self.append_flags(flag)

        # the surface to draw on
        self._surface = surface

    def _draw_solid_polygons(self, points, sizes, colors):
        self._draw_polygons_impl(points, sizes, colors, 0)

    def _draw_polygons(self, points, sizes, colors):
        self._draw_polygons_impl(points, sizes, colors, 1)

    def _draw_polygons_impl(self, points, sizes, colors, lw):

        n_polygons = sizes.shape[0]
        start = 0
        for i in range(n_polygons):
            s = sizes[i]
            p = points[start : start + s, :]
            pygame.draw.polygon(self._surface, colors[i, :], p, lw)
            start += s

    def _draw_solid_circles(self, centers, radii, axis, colors):

        # draw circles itself
        self._draw_circles_impl(centers, radii, colors, lw=0)

        p = centers - numpy.flip(axis, 1) * radii[:, None]

        n = centers.shape[0]
        for i in range(n):
            pygame.draw.line(
                self._surface, (colors[i, :] * 0.5), centers[i, ...], p[i, ...]
            )

    def _draw_circles(self, centers, radii, colors):
        self._draw_circles_impl(centers, radii, colors, lw=1)

    def _draw_circles_impl(self, centers, radii, colors, lw):
        n = centers.shape[0]
        for i in range(n):
            pygame.draw.circle(self._surface, colors[i, :], centers[i, :], radii[i], lw)

    def _draw_points(self, centers, sizes, colors):
        pass

    def _draw_segments(self, points, colors):
        n = points.shape[0]
        for i in range(n):
            pygame.draw.line(
                self._surface, colors[i, :], points[i, 0, :], points[i, 1, :]
            )

    def _draw_particles(self, centers, radius, colors=None):
        default_color = (255, 255, 255, 255)

        n_particles = centers.shape[0]
        centers -= radius
        d = 2 * radius
        d = max(1, d)
        for i in range(n_particles):

            if colors is None:
                c = default_color
            else:
                c = colors[i, :]

            pygame.draw.rect(self._surface, c, (centers[i, 0], centers[i, 1], d, d))

    def _uint8_color(self, color):
        return [c * 255 for c in color]

    def _line_width(self, line_width):
        screen_line_width = int(self.world_to_screen_scale(line_width) + 0.5)
        return max(1, screen_line_width)

    # non-batch api
    def draw_solid_circle(self, center, radius, axis, color):
        screen_center = self.world_to_screen(center)
        screen_radius = self.world_to_screen_scale(radius)
        screen_color = self._uint8_color(color)
        pygame.draw.circle(self._surface, screen_color, screen_center, screen_radius, 0)

    def draw_circle(self, center, radius, color, line_width=1):
        screen_center = self.world_to_screen(center)
        screen_radius = self.world_to_screen_scale(radius)
        screen_line_width = self._line_width(line_width)
        screen_color = self._uint8_color(color)
        pygame.draw.circle(
            self._surface, screen_color, screen_center, screen_radius, screen_line_width
        )

    def draw_segment(self, p1, p2, color, line_width=1):
        screen_p1 = self.world_to_screen(p1)
        screen_p2 = self.world_to_screen(p2)
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)
        pygame.draw.line(
            self._surface, screen_color, screen_p1, screen_p2, screen_line_width
        )

    def draw_polygon(self, vertices, color, line_width=1):
        # todo add C++ function for this
        screen_vertices = [self.world_to_screen(v) for v in vertices]
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)
        pygame.draw.polygon(
            self._surface, screen_color, screen_vertices, screen_line_width
        )

    def draw_solid_polygon(self, vertices, color):
        # todo add C++ function for this
        screen_vertices = [self.world_to_screen(v) for v in vertices]
        screen_color = self._uint8_color(color)
        pygame.draw.polygon(self._surface, screen_color, screen_vertices, 0)
