#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
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

from math import cos, sin

from .framework import (Framework, main)
from pybox2d import (circle_shape, edge_shape, fixture_def, polygon_shape,
                   math.pi)


class CharacterCollision(Framework):
    name = "Character Collision"
    description = ("This tests various character collision shapes.\n"
                   "Limitation: Square and hexagon can snag on aligned boxes.\n"
                   "Feature: Loops have smooth collision, inside and out."
                   )

    def __init__(self):
        super(CharacterCollision, self).__init__()

        ground = self.world.create_static_body(
            position=(0, 0),
            shapes=edge_shape(vertices=[(-20, 0), (20, 0)])
        )

        # Collinear edges
        self.world.create_static_body(
            shapes=[edge_shape(vertices=[(-8, 1), (-6, 1)]),
                    edge_shape(vertices=[(-6, 1), (-4, 1)]),
                    edge_shape(vertices=[(-4, 1), (-2, 1)]),
                    ]
        )

        # Square tiles
        self.world.create_static_body(
            shapes=[polygon_shape(box=[1, 1, (4, 3), 0]),
                    polygon_shape(box=[1, 1, (6, 3), 0]),
                    polygon_shape(box=[1, 1, (8, 3), 0]),
                    ]
        )

        # Square made from an edge loop. Collision should be smooth.
        body = self.world.create_static_body()
        body.CreateLoopFixture(vertices=[(-1, 3), (1, 3), (1, 5), (-1, 5)])

        # Edge loop.
        body = self.world.create_static_body(position=(-10, 4))
        body.CreateLoopFixture(vertices=[
            (0.0, 0.0), (6.0, 0.0),
            (6.0, 2.0), (4.0, 1.0),
            (2.0, 2.0), (0.0, 2.0),
            (-2.0, 2.0), (-4.0, 3.0),
            (-6.0, 2.0), (-6.0, 0.0), ]
        )

        # Square character 1
        self.world.create_dynamic_body(
            position=(-3, 8),
            fixedRotation=True,
            allow_sleep=False,
            fixtures=fixture_def(shape=polygon_shape(
                box=(0.5, 0.5)), density=20.0),
        )

        # Square character 2
        body = self.world.create_dynamic_body(
            position=(-5, 5),
            fixedRotation=True,
            allow_sleep=False,
        )

        body.create_polygon_fixture(box=(0.25, 0.25), density=20.0)

        # Hexagon character
        a = math.pi / 3.0
        self.world.create_dynamic_body(
            position=(-5, 8),
            fixedRotation=True,
            allow_sleep=False,
            fixtures=fixture_def(
                shape=polygon_shape(
                    vertices=[(0.5 * cos(i * a), 0.5 * sin(i * a))
                              for i in range(6)]),
                density=20.0
            ),
        )

        # Circle character
        self.world.create_dynamic_body(
            position=(3, 5),
            fixedRotation=True,
            allow_sleep=False,
            fixtures=fixture_def(
                shape=circle_shape(radius=0.5),
                density=20.0
            ),
        )

    def Step(self, settings):
        super(CharacterCollision, self).Step(settings)
        pass

if __name__ == "__main__":
    main(CharacterCollision)
