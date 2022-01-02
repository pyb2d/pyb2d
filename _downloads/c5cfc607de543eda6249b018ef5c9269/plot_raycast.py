"""
Raycast
===========================

This example shows how to use raycasting
"""

from b2d.testbed import TestbedBase
import random
import numpy as np
import b2d


def rand_color():
    return tuple([random.random() for i in range(3)])


class RayCastCallback(b2d.RayCastCallback):
    def __init__(self):
        super(RayCastCallback, self).__init__()
        self._touched_circles = []

    def report_fixture(self, fixture, point, normal, fraction):
        user_data = fixture.body.user_data
        if user_data is not None:
            self._touched_circles.append(user_data)
            return fraction
        return -1


class Raycast(TestbedBase):

    name = "raycast"

    def __init__(self, settings=None):
        super(Raycast, self).__init__(settings=settings)
        dimensions = [30, 30]

        # the outer box
        box_shape = b2d.ChainShape()
        box_shape.create_loop(
            [
                (0, 0),
                (0, dimensions[1]),
                (dimensions[0], dimensions[1]),
                (dimensions[0], 0),
            ]
        )
        box = self.world.create_static_body(
            position=(0, 0), fixtures=b2d.fixture_def(shape=box_shape, friction=1)
        )

        self.magic_circle_rad = 1.0
        self.magic_circle = self.world.create_dynamic_body(
            position=[1, 1],
            fixtures=b2d.fixture_def(
                shape=b2d.circle_shape(radius=self.magic_circle_rad),
                density=1.0,
                friction=1.0,
            ),
        )

        self.circles = []
        for i in range(10):
            self.circles.append(
                self.world.create_dynamic_body(
                    position=[s / 2 + random.random() for s in dimensions],
                    fixtures=b2d.fixture_def(
                        shape=b2d.circle_shape(radius=1), density=1.0, friction=1.0
                    ),
                    user_data=i,
                )
            )
        self._touched_circles = []

    def post_step(self, dt):
        self._touched_circles = []
        pos = self.magic_circle.position

        n = 5
        r0 = self.magic_circle_rad
        r1 = 5

        # most of this can be precomuted
        t = np.linspace(0, 2 * np.pi, n, endpoint=False)
        x0 = r0 * np.cos(t) + pos[0]
        y0 = r0 * np.sin(t) + pos[1]
        x1 = r1 * np.cos(t) + pos[0]
        y1 = r1 * np.sin(t) + pos[1]

        for i in range(n):
            p0 = float(x0[i]), float(y0[i])
            p1 = float(x1[i]), float(y1[i])

            cb = RayCastCallback()
            self.debug_draw.draw_segment(p0, p1, (1, 1, 1), line_width=0.1)
            self.world.ray_cast(cb, p0, p1)
            self._touched_circles.extend(cb._touched_circles)

    def post_debug_draw(self):

        position = tuple(self.magic_circle.position)
        self.debug_draw.draw_solid_circle(position, 1.0, (1, 0), rand_color())

        for i in self._touched_circles:
            self.debug_draw.draw_solid_circle(
                self.circles[i].position, 1.0, (1, 0), (1, 0, 0)
            )


if __name__ == "__main__":

    ani = b2d.testbed.run(Raycast)
    ani
