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
from pybox2d import (edge_shape, fixture_def, polygon_shape)


class Mobile (Framework):
    name = "Mobile"
    max_depth = 4

    def __init__(self):
        Framework.__init__(self)

        ground = self.world.create_static_body(
            position=(0, 20),
            shapes=[edge_shape(vertices=[(-20, 0), (20, 0)])],
        )

        a = 0.5
        depth = 0
        self.root = self.add_node(ground, (0, 0), depth, 3.0, a)

        self.world.create_revolute_joint(body_a=ground, body_b=self.root,
                                       local_anchor_a=(0, 0), local_anchor_b=(0, a))

    def add_node(self, parent, local_anchor, depth, offset, a):
        density = 20.0
        h = (0, a)

        p = parent.position + local_anchor - h

        fixture = fixture_def(shape=polygon_shape(box=(0.25 * a, a)),
                               density=density)
        body = self.world.create_dynamic_body(position=p, fixtures=fixture)

        if depth == self.max_depth:
            return body

        a1 = (offset, -a)
        a2 = (-offset, -a)
        body1 = self.add_node(body, a1, depth + 1, 0.5 * offset, a)
        body2 = self.add_node(body, a2, depth + 1, 0.5 * offset, a)

        self.world.create_revolute_joint(body_a=body, body_b=body1,
                                       local_anchor_a=a1, local_anchor_b=h)
        self.world.create_revolute_joint(body_a=body, body_b=body2,
                                       local_anchor_a=a2, local_anchor_b=h)

        return body

if __name__ == "__main__":
    main(Mobile)
