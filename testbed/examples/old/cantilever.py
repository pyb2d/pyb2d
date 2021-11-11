#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version by Ken Lauer / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from .framework import (Framework, main)
from pybox2d import (circle_shape, edge_shape, fixture_def, polygon_shape)


class Cantilever (Framework):
    name = "Cantilever"
    description = ""
    numPlanks = 8

    def __init__(self):
        super(Cantilever, self).__init__()

        # The ground
        ground = self.world.create_body(
            shapes=edge_shape(vertices=[(-40, 0), (40, 0)]))

        plank = fixture_def(
            shape=polygon_shape(box=(0.5, 0.125)),
            friction=0.2,
            density=20
        )

        # Create one cantilever (Only the left end is fixed)
        prevBody = ground
        for i in range(self.numPlanks):
            body = self.world.create_dynamic_body(
                position=(-14.5 + i, 5),
                fixtures=plank,
            )

            self.world.CreateWeldJoint(
                body_a=prevBody,
                body_b=body,
                anchor=(-15 + i, 5),
            )

            prevBody = body

        # Create another higher up
        prevBody = ground
        for i in range(self.numPlanks):
            body = self.world.create_dynamic_body(
                position=(-14.5 + i, 15),
                fixtures=plank,
            )

            self.world.CreateWeldJoint(
                body_a=prevBody,
                body_b=body,
                anchor=(-15 + i, 15),
            )

            prevBody = body

        # And the left-most unconnected one (technically not a cantilever)
        prevBody = ground
        for i in range(self.numPlanks):
            body = self.world.create_dynamic_body(
                position=(-4.5 + i, 5),
                fixtures=plank,
            )

            if i > 0:  # skip the joint on the first one
                self.world.CreateWeldJoint(
                    body_a=prevBody,
                    body_b=body,
                    anchor=(-5 + i, 5),
                )

            prevBody = body

        # And the right-most unconnected one, using joint damping
        prevBody = ground
        for i in range(self.numPlanks):
            body = self.world.create_dynamic_body(
                position=(5.5 + i, 10),
                fixtures=plank,
            )

            if i > 0:  # skip the joint on the first one
                self.world.CreateWeldJoint(
                    body_a=prevBody,
                    body_b=body,
                    anchor=(5 + i, 10),
                    frequency_hz=8.0,
                    damping_ratio=0.7,
                )

            prevBody = body

        # And a few random shapes to play with
        # First a set of triangles,
        fixture = fixture_def(shape=polygon_shape(vertices=[(-0.5, 0.0),
                                                              (0.5, 0.0),
                                                              (0.0, 1.5),
                                                              ]),
                               density=1.0)
        for i in range(2):
            self.world.create_dynamic_body(
                position=(-8 + 8 * i, 12),
                fixtures=fixture,
            )

        # And then a few circles
        fixture = fixture_def(shape=circle_shape(radius=0.5), density=1)
        for i in range(3):
            self.world.create_dynamic_body(
                position=(-6 + 6 * i, 10),
                fixtures=fixture,
            )


if __name__ == "__main__":
    main(Cantilever)
