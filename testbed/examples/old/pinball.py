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

from .framework import (Framework, Keys, main)
from pybox2d import (circle_shape, fixture_def, b2LoopShape, polygon_shape,
                   b2RevoluteJointDef)


class Pinball (Framework):
    name = "Pinball"
    description = ('This tests bullet collision and provides an example of a gameplay scenario.\n'
                   'Press A to control the flippers.')
    bodies = []
    joints = []

    def __init__(self):
        super(Pinball, self).__init__()

        # The ground
        ground = self.world.create_body(
            shapes=b2LoopShape(vertices=[(0, -2), (8, 6),
                                         (8, 20), (-8, 20),
                                         (-8, 6)]),
        )

        # Flippers
        p1, p2 = (-2, 0), (2, 0)

        fixture = fixture_def(shape=polygon_shape(box=(1.75, 0.1)), density=1)
        flipper = {'fixtures': fixture}

        self.leftFlipper = self.world.create_dynamic_body(
            position=p1,
            **flipper
        )
        self.rightFlipper = self.world.create_dynamic_body(
            position=p2,
            **flipper
        )

        rjd = b2RevoluteJointDef(
            body_a=ground,
            body_b=self.leftFlipper,
            local_anchor_a=p1,
            local_anchor_b=(0, 0),
            enable_motor=True,
            enable_limit=True,
            max_motor_torque=1000,
            motor_speed=0,
            lower_angle=-30.0 * math.pi / 180.0,
            upper_angle=5.0 * math.pi / 180.0,
        )

        self.leftJoint = self.world.create_joint(rjd)

        rjd.motor_speed = 0
        rjd.local_anchor_a = p2
        rjd.body_b = self.rightFlipper
        rjd.lower_angle = -5.0 * math.pi / 180.0
        rjd.upper_angle = 30.0 * math.pi / 180.0
        self.rightJoint = self.world.create_joint(rjd)

        # Ball
        self.ball = self.world.create_dynamic_body(
            fixtures=fixture_def(
                shape=circle_shape(radius=0.2),
                density=1.0),
            bullet=True,
            position=(1, 15))

        self.pressed = False

    def Keyboard(self, key):
        if key == Keys.K_a:
            self.pressed = True

    def KeyboardUp(self, key):
        if key == Keys.K_a:
            self.pressed = False

    def Step(self, settings):
        if self.pressed:
            self.leftJoint.motor_speed = 20
            self.rightJoint.motor_speed = -20
        else:
            self.leftJoint.motor_speed = -10
            self.rightJoint.motor_speed = 10
        super(Pinball, self).Step(settings)

if __name__ == "__main__":
    main(Pinball)
