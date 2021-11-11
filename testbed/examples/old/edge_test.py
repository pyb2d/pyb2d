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

from .framework import (Framework, main)
from pybox2d import (edge_shape, polygon_shape)


class EdgeTest (Framework):
    name = "EdgeTest"
    description = "Utilizes edge_shape"

    def __init__(self):
        super(EdgeTest, self).__init__()

        v1 = (-10.0, 0.0)
        v2 = (-7.0, -1.0)
        v3 = (-4.0, 0.0)
        v4 = (0.0, 0.0)
        v5 = (4.0, 0.0)
        v6 = (7.0, 1.0)
        v7 = (10.0, 0.0)

        shapes = [edge_shape(vertices=[None, v1, v2, v3]),
                  edge_shape(vertices=[v1, v2, v3, v4]),
                  edge_shape(vertices=[v2, v3, v4, v5]),
                  edge_shape(vertices=[v3, v4, v5, v6]),
                  edge_shape(vertices=[v4, v5, v6, v7]),
                  edge_shape(vertices=[v5, v6, v7])
                  ]
        ground = self.world.create_static_body(shapes=shapes)

        box = self.world.create_dynamic_body(
            position=(0.5, 0.6),
            allow_sleep=False,
            shapes=polygon_shape(box=(0.5, 0.5))
        )

if __name__ == "__main__":
    main(EdgeTest)
