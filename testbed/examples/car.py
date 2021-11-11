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

from pybox2d.framework import Framework,Testbed

from bridge import create_bridge
import math
from math import sqrt

from pybox2d import (circle_shape, edge_shape, fixture_def, polygon_shape)


def create_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(1.0, 1.0), chassis_vertices=None,
               wheel_axis=(0.0, 1.0), wheel_torques=[20.0, 10.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    """
    """
    x_offset, y_offset = offset
    scale_x, scale_y = scale
    if chassis_vertices is None:
        chassis_vertices = [
            (-1.5, -0.5),
            (1.5, -0.5),
            (1.5, 0.0),
            (0.0, 0.9),
            (-1.15, 0.9),
            (-1.5, 0.2),
        ]

    chassis_vertices = [(scale_x * x, scale_y * y)
                        for x, y in chassis_vertices]
    radius_scale = sqrt(scale_x ** 2 + scale_y ** 2)
    wheel_radius *= radius_scale

    chassis = world.create_dynamic_body(
        position=(x_offset, y_offset),
        fixtures=fixture_def(
            shape=polygon_shape(vertices=chassis_vertices),
            density=density,
        )
    )

    wheels, springs = [], []
    wheel_xs = [-wheel_separation * scale_x /
                2.0, wheel_separation * scale_x / 2.0]
    for x, torque, drive in zip(wheel_xs, wheel_torques, wheel_drives):
        wheel = world.create_dynamic_body(
            position=(x_offset + x, y_offset - wheel_radius),
            fixtures=fixture_def(
                shape=circle_shape(radius=wheel_radius),
                density=density,
            )
        )

        spring = world.create_wheel_joint(
            body_a=chassis,
            body_b=wheel,
            anchor=wheel.position,
            local_axis_a=wheel_axis,
            motor_speed=0.0,
            max_motor_torque=torque,
            enable_motor=drive,
            # stiffness=hz,
            # damping=zeta
        )

        wheels.append(wheel)
        springs.append(spring)

    return chassis, wheels, springs


class Car (Framework):
    name = "Car"
    description = "Keys: left = a, brake = s, right = d, hz down = q, hz up = e"
    hz = 20
    zeta = 0.7
    speed = 50
    bridgePlanks = 20

    def __init__(self, gui):
        super(Car, self).__init__(gui)

        # The ground -- create some terrain
        ground = self.world.create_static_body(
            shapes=edge_shape(vertices=[(-20, 0), (20, 0)])
        )

        x, y1, dx = 20, 0, 5
        vertices = [0.25, 1, 4, 0, 0, -1, -2, -2, -1.25, 0]
        for y2 in vertices * 2:  # iterate through vertices twice
            # ground.create_edge_chain_fixture(
            #     vertices=[(x, y1), (x + dx, y2)],
            #     density=0,
            #     friction=0.6,
            # )
            y1 = y2
            x += dx

        x_offsets = [0, 80, 40, 20, 40]
        x_lengths = [40, 40, 10, 40, 0]
        y2s = [0, 0, 5, 0, 20]

        for x_offset, x_length, y2 in zip(x_offsets, x_lengths, y2s):
            x += x_offset
            # ground.create_edge_chain_fixture(
            #     vertices=[(x, 0), (x + x_length, y2)],
            #     density=0,
            #     friction=0.6,
            # )

        # Teeter
        body = self.world.create_dynamic_body(
            position=(140, 0.90),
            fixtures=fixture_def(
                shape=polygon_shape(box=(10, 0.25)),
                density=1.0,
            )
        )

        self.world.create_revolute_joint(
            body_a=ground,
            body_b=body,
            anchor=body.position,
            lower_angle=-8.0 * math.pi / 180.0,
            upper_angle=8.0 * math.pi / 180.0,
            enable_limit=True,
        )

        # Bridge
        create_bridge(self.world, ground, (2.0, 0.25),
                      (161.0, -0.125), self.bridgePlanks)

        # Boxes
        for y_pos in [0.5, 1.5, 2.5, 3.5, 4.5]:
            self.world.create_dynamic_body(
                position=(230, y_pos),
                fixtures=fixture_def(
                    shape=polygon_shape(box=(0.5, 0.5)),
                    density=0.5,
                )
            )

        car, wheels, springs = create_car(self.world, offset=(
            0.0, 1.0), wheel_radius=0.4, wheel_separation=2.0, scale=(1, 1))
        self.car = car
        self.wheels = wheels
        self.springs = springs

    def _handle_key_interaction(self):
        if self.is_key_down('A'):
            self.springs[0].motor_speed = self.speed
        if self.is_key_down('S'):
            self.springs[0].motor_speed = 0
        if self.is_key_down('D'):
            self.springs[0].motor_speed = -self.speed
        if self.is_key_down('E') or self.is_key_down('Q'):
            if self.is_key_down('Q'):
                self.hz = max(0, self.hz - 1.0)
            else:
                self.hz += 1.0

            for spring in self.springs:
                spring.stiffness = self.hz
    def pre_step(self, dt):
        self._handle_key_interaction()
    # def step(self), settings):
    #     super(Car, self).Step(settings)
    #     self.viewCenter = (self.car.position.x, 20)
    #     #self.Print("frequency = %g hz, damping ratio = %g" %
    #     #           (self.hz, self.zeta))


if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(Car)
    testbed.run()

