import numpy as np
import b2d
import cv2 as cv


class OpenCvBatchDebugDraw(b2d.batch_debug_draw_cls(False, True, True)):
    def __init__(self, image, flags=None):
        super(OpenCvBatchDebugDraw, self).__init__()

        # what is drawn
        if flags is None:
            flags = [
                "shape",
                "joint",
                "particle",
            ]  # ,'aabb','pair','center_of_mass','particle']
        self.flags = flags
        self.clear_flags(
            ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        )
        for flag in flags:
            self.append_flags(flag)

        # the image to draw on
        self._image = image

    def _draw_solid_polygons(self, points, sizes, colors):
        self._draw_polygons_impl(points, sizes, colors, True)

    def _draw_polygons(self, points, sizes, colors):
        self._draw_polygons_impl(points, sizes, colors, False)

    def _draw_polygons_impl(self, points, sizes, colors, fill):
        line_type = 8
        n_polygons = sizes.shape[0]
        start = 0
        points = np.flip(points, axis=1)
        for i in range(n_polygons):
            s = sizes[i]
            p = points[start : start + s, :].astype("int32")
            color = tuple(map(int, colors[i, :]))
            if fill:
                cv.fillPoly(self._image, [p], color, line_type)
            else:
                cv.polylines(self._image, [p], True, color, line_type)
            start += s

    def _draw_solid_circles(self, centers, radii, axis, colors):
        self._draw_circles_impl(centers, radii, colors, axis=axis, lw=-1)

    def _draw_circles(self, centers, radii, colors):
        self._draw_circles_impl(centers, radii, colors, axis=None, lw=1)

    def _draw_circles_impl(self, centers, radii, colors, axis, lw):
        line_type = 8
        thickness = 1
        n = centers.shape[0]
        centers = np.flip(centers, axis=1)
        # centers = centers.swapxes(0,1)
        for i in range(n):
            color = tuple(map(int, colors[i, :]))
            cv.circle(
                self._image,
                centers[i, :].astype("int32"),
                radii[i].astype("int32"),
                color,
                lw,
                line_type,
            )

        if axis is not None:
            p = centers - axis * radii[:, None]

            n = centers.shape[0]
            for i in range(n):
                color = tuple(map(int, colors[i, :] * 0.75))
                cv.line(
                    self._image,
                    centers[i, ...].astype("int32"),
                    p[i, ...].astype("int32"),
                    color,
                )

    def _draw_points(self, centers, sizes, colors):
        pass

    def _draw_segments(self, points, colors):
        line_type = 8
        thickness = 1
        points = np.flip(points, axis=2)
        n = points.shape[0]
        for i in range(n):
            color = tuple(map(int, colors[i, :]))
            cv.line(
                self._image,
                points[i, 0, :].astype("int32"),
                points[i, 1, :].astype("int32"),
                color,
            )

    def _draw_particles(self, centers, radius, colors=None):
        radius = min(1, radius)
        default_color = (255, 255, 255, 255)
        centers = np.flip(centers, axis=1)
        n_particles = centers.shape[0]
        centers -= radius
        d = 2 * radius
        for i in range(n_particles):

            if colors is None:
                color = default_color
            else:
                color = tuple(map(int, colors[i, :]))

            p0 = (centers[i, :] - radius).astype("int32")
            p1 = (p0 + 2 * radius).astype("int32")
            cv.rectangle(self._image, p0, p1, color, -1)

    def _uint8_color(self, color):
        return tuple(int(c * 255) for c in color)

    def _line_width(self, line_width):
        screen_line_width = int(self.world_to_screen_scale(line_width) + 0.5)
        return max(1, screen_line_width)

    def _point(self, point):
        return int(point[1]), int(point[0])

    def _draw_circle(self, center, radius, color, line_width):
        screen_center = self._point(self.world_to_screen(center))
        screen_radius = int(self.world_to_screen_scale(radius) + 0.5)
        screen_color = self._uint8_color(color)

        line_type = 8
        cv.circle(
            self._image,
            screen_center,
            screen_radius,
            screen_color,
            line_width,
            line_type,
        )

    # non-batch api
    def draw_solid_circle(self, center, radius, axis, color):
        self._draw_circle(center, radius, color, -1)

    def draw_circle(self, center, radius, color, line_width=1):
        screen_line_width = self._line_width(line_width)
        self._draw_circle(center, radius, color, screen_line_width)

    def draw_segment(self, p1, p2, color, line_width=1):
        screen_p1 = self._point(self.world_to_screen(p1))
        screen_p2 = self._point(self.world_to_screen(p2))
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)

        cv.line(self._image, screen_p1, screen_p2, screen_color, screen_line_width)

    def draw_polygon(self, vertices, color, line_width=1):
        # todo add C++ function for this
        screen_vertices = np.array(
            [self._point(self.world_to_screen(v)) for v in vertices], dtype="int32"
        )
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)

        cv.polylines(
            self._image, [screen_vertices], True, screen_color, screen_line_width, 8
        )

    def draw_solid_polygon(self, vertices, color):
        # todo add C++ function for this
        screen_vertices = np.array(
            [self._point(self.world_to_screen(v)) for v in vertices], dtype="int32"
        )
        screen_color = self._uint8_color(color)

        cv.fillPoly(self._image, [screen_vertices], screen_color, 8)
