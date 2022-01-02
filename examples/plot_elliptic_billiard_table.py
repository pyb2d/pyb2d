"""
Function Shape
===========================

This example show how to create a shape from a mathematical function.
In this example we use f(x) = sin(x) + log(x) + 5.5
"""

from b2d.testbed import TestbedBase
import random
import numpy as np
import b2d
import math


def ellipse_chain_shape(positon, a, b, n=50):

    t = np.linspace(start=0, stop=2.0 * math.pi, num=n + 1)
    x = (a * np.cos(t) + positon[0])[:-1]
    y = (b * np.sin(t) + positon[1])[:-1]
    verts = np.stack([x, y], -1)
    verts = np.require(verts, requirements=["C"])
    return b2d.loop_shape(np.flip(verts, axis=0))


class EllipticBillardTable(TestbedBase):

    name = "EllipticBillardTable"

    def __init__(self, settings=None):
        super(EllipticBillardTable, self).__init__(settings=settings, gravity=(0, 0))

        self.a = 20
        self.b = 10

        e = np.sqrt(self.a ** 2 - self.b ** 2)
        center = (self.a, self.b)
        shape = ellipse_chain_shape(center, self.a, self.b, n=50)
        self.f0 = center[0] - e, center[1]
        self.f1 = center[0] + e, center[1]
        box = self.world.create_static_body(position=(0, 0), shape=shape)

        for i in range(1):
            box = self.world.create_dynamic_body(
                position=self.f1,
                fixtures=b2d.fixture_def(
                    shape=b2d.circle_shape(
                        pos=(0, 0),
                        radius=1,
                    ),
                    density=1.0,
                    restitution=0.9,
                ),
                fixed_rotation=True,
                linear_damping=0.1,
            )

    def pre_debug_draw(self):
        # focal points
        self.debug_draw.draw_circle(self.f0, 1, color=(0, 1, 0), line_width=0.1)
        self.debug_draw.draw_circle(self.f1, 1, color=(0, 1, 0), line_width=0.1)


if __name__ == "__main__":

    ani = b2d.testbed.run(EllipticBillardTable)
    ani
