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

from framework import Framework,Testbed
from pybox2d import *
import math
# b2_pi
# Original inspired by a contribution by roman_m
# Dimensions scooped from APE (http://www.cove.org/ape/index.htm)


class TheoJansen (Framework):
    name = "Theo Jansen"
    description = "Keys: left = a, brake = s, right = d, toggle motor = m"
    motor_speed = 3
    motorOn = True
    offset = vec2(0, 8.0)

    def __init__(self, gui):
        super(TheoJansen, self).__init__(gui=gui)

        #
        ball_count = 40
        pivot = vec2(0, 0.8)

        # The ground
        ground = self.world.create_static_body(
            shapes=[
                edge_shape(vertices=[(-50, -0), (50, -0)]),
                edge_shape(vertices=[(-50, -0), (-50, 0)]),
                edge_shape(vertices=[(50, -0), (50, 0)]),
            ]
        )
        
        box = fixture_def(
            shape=polygon_shape(box=(0.5, 0.5)),
            density=1,
            friction=0.3)
        circle = fixture_def(
            shape=circle_shape(radius=0.25),
            density=1)

        # Create the balls on the ground
        for i in range(ball_count):
            self.world.create_dynamic_body(
                fixtures=circle,
                position=vec2(-40 + 2.0 * i, 0.5),
            )

        # The chassis
        chassis_fixture = fixture_def(
            shape=polygon_shape(box=(2.5, 1)),
            density=1,
            friction=0.3,
            group_index=-1)

        self.chassis = self.world.create_dynamic_body(
            fixtures=chassis_fixture,
            position=pivot + self.offset)

        # Chassis wheel
        wheel_fixture = fixture_def(
            shape=circle_shape(radius=1.6),
            density=1,
            friction=0.3,
            group_index=-1)

        self.wheel = self.world.create_dynamic_body(
            fixtures=wheel_fixture,
            position=pivot + self.offset)

        #Add a joint between the chassis wheel and the chassis itself
        self.motorJoint = self.world.create_revolute_joint(
            body_a=self.wheel,
            body_b=self.chassis,
            anchor=pivot + self.offset,
            collide_connected=False,
            motor_speed=self.motor_speed,
            max_motor_torque=400,
            enable_motor=self.motorOn)

        
  
        wheelAnchor = pivot + vec2(0, -0.8)
        self.CreateLeg(-1, wheelAnchor)
        #self.CreateLeg(1, wheelAnchor)
    
       

        self.wheel.transform = transform(self.wheel.position, 120.0 * math.pi / 180)
        self.CreateLeg(-1, wheelAnchor)
        self.CreateLeg(1, wheelAnchor)

        self.wheel.transform = transform(self.wheel.position, -120.0 * math.pi / 180)
        self.CreateLeg(-1, wheelAnchor)
        self.CreateLeg(1, wheelAnchor)

    def CreateLeg(self, s, wheelAnchor):

        p1 = vec2(5.4 * s, -6.1)
        p2 = vec2(7.2 * s, -1.2)
        p3 = vec2(4.3 * s, -1.9)
        p4 = vec2(3.1 * s, 0.8)
        p5 = vec2(6.0 * s, 1.5)
        p6 = vec2(2.5 * s, 3.7)

        # Use a simple system to create mirrored vertices
        if s > 0:
            poly1 = polygon_shape(vertices=(p1, p2, p3))
            poly2 = polygon_shape(vertices=((0, 0), p5 - p4, p6 - p4))
        else:
            poly1 = polygon_shape(vertices=(p1, p3, p2))
            poly2 = polygon_shape(vertices=((0, 0), p6 - p4, p5 - p4))

        #print("body one pos",self.offset)
        body1 = self.world.create_dynamic_body(
            position=self.offset,
            angular_damping=10,
            fixtures=fixture_def(
                shape=poly1,
                group_index=-1,
                density=1),
        )

        body2 = self.world.create_dynamic_body(
            position=p4 + self.offset,
            angular_damping=10,
            fixtures=fixture_def(
                shape=poly2,
                group_index=-1,
                density=1),
        )

        # Using a soft distance constraint can reduce some jitter.
        # It also makes the structure seem a bit more fluid by
        # acting like a suspension system.
        # Now, join all of the bodies together with distance joints,
        # and one single revolute joint on the chassis
        # print("anchor_a",p2 + self.offset)
        # print("anchor_b",p5 + self.offset)
        self.world.create_distance_joint(
            damping_ratio=0.5,
            frequency_hz=10,
            body_a=body1, body_b=body2,
            anchor_a=p2 + self.offset,
            anchor_b=p5 + self.offset,
        )

        self.world.create_distance_joint(
            damping_ratio=0.5,
            frequency_hz=10,
            body_a=body1, body_b=body2,
            anchor_a=p3 + self.offset,
            anchor_b=p4 + self.offset,
        )

        self.world.create_distance_joint(
            damping_ratio=0.5,
            frequency_hz=10,
            body_a=body1, body_b=self.wheel,
            anchor_a=p3 + self.offset,
            anchor_b=wheelAnchor + self.offset,
        )

      
        self.world.create_distance_joint(
            damping_ratio=0.5,
            frequency_hz=10,
            body_a=body2, body_b=self.wheel,
            anchor_a=p6 + self.offset,
            anchor_b=wheelAnchor + self.offset,
        )

        self.world.create_revolute_joint(
            body_a=body2,
            body_b=self.chassis,
            anchor=p4 + self.offset,
        )

    def Keyboard(self, key):
        if key == Keys.K_a:
            self.motorJoint.motor_speed = -self.motor_speed
        elif key == Keys.K_d:
            self.motorJoint.motor_speed = self.motor_speed
        elif key == Keys.K_s:
            self.motorJoint.motor_speed = 0
        elif key == Keys.K_m:
            self.motorJoint.motorEnabled = not self.motorJoint.motorEnabled

if __name__ == "__main__":
    testbed = Testbed(guiType='pg')
    testbed.setExample(TheoJansen)
    testbed.run()
