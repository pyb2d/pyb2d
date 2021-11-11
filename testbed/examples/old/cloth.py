#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
#
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlecode.com)
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

# Ported from the Cloth test by Paril, originally for Box2CS:
#   http://www.box2d.org/forum/viewtopic.php?f=6&t=6124
#
from .framework import (Framework, Keys, main)
from pybox2d import (circle_shape, fixture_def, b2Random, vec2)


def create_cloth(world, segment_count, body_size, position=(0, 30),
                 group_index=-1, bar_height=0.5, base_hz=15,
                 base_damping=0.11, density=0.2):
    segment_w, segment_h = segment_count
    body_spacing_w = body_size * 2
    total_w = body_spacing_w * segment_w
    position = vec2(*position)

    # The static bar at the top which holds the cloth
    bar = world.create_static_body(position=position)
    bar.create_polygon_fixture(box=(total_w / 2.0 + body_spacing_w,
                                  bar_height / 2.0),
                             groupIndex=group_index)

    box_fixture = fixture_def(shape=circle_shape(radius=body_size),
                               groupIndex=group_index, density=density)

    weld_joints = []
    distance_joints = []
    cloth = [[None] * segment_h for x in range(segment_w)]
    for y in range(segment_h):
        pos = position - (total_w / 2.0, y * body_spacing_w)
        for x in range(segment_w):
            pos += (body_spacing_w, 0.0)
            body = world.create_dynamic_body(position=pos, fixtures=box_fixture)
            cloth[x][y] = body

            if y == 0:
                joint = world.CreateWeldJoint(body_a=body, body_b=bar,
                                              anchor=body.position)
                weld_joints.append(joint)

    connect_bodies = []
    for y in range(segment_h):
        for x in range(segment_w):
            if x <= segment_w - 2:
                left_body = cloth[x][y]
                right_body = cloth[x + 1][y]
                connect_bodies.append((left_body, right_body))
            if y > 0:
                left_body = cloth[x][y]
                right_body = cloth[x][y - 1]
                connect_bodies.append((left_body, right_body))

    for body_a, body_b in connect_bodies:
        joint = world.CreateDistanceJoint(
            body_a=body_a,
            body_b=body_b,
            anchorA=body_a.position,
            anchorB=body_b.position,
            frequency_hz=base_hz + b2Random(0, base_hz / 2.0),
            damping_ratio=base_damping + b2Random(0.01, base_damping),
        )
        distance_joints.append(joint)

    return cloth, weld_joints, distance_joints


def step_cloth(world, cloth, wind, body_size, segment_count, distance_joints,
               wind_dir=(1, 1), wind_rand=0.0, distance_factor=1.45):
    segment_w, segment_h = segment_count
    body_spacing_w = body_size * 2
    if wind:
        for x in range(segment_w):
            w = (b2Random(wind_dir[0] - wind_rand / 2.0,
                          wind_dir[0] + wind_rand / 2.0),
                 b2Random(wind_dir[1] - wind_rand / 2.0,
                          wind_dir[1] + wind_rand / 2.0))
            cloth[x][-1].linearVelocity += w

    # If any two points are too far from one another, find the joint connecting
    # them and destroy it.
    check_segments = []
    for y in range(segment_h):
        for x in range(segment_w):
            if y > 0:
                check_segments.append((cloth[x][y], cloth[x][y - 1]))
            if x <= segment_w - 2:
                check_segments.append((cloth[x][y], cloth[x + 1][y]))

    thresh = body_spacing_w * distance_factor
    for c1, c2 in check_segments:
        if (c1.worldCenter - c2.worldCenter).length <= thresh:
            continue

        for joint in distance_joints:
            if ((joint.body_a == c1 and joint.body_b == c2) or
                    (joint.body_a == c2 and joint.body_b == c1)):
                world.destroy_joint(joint)
                distance_joints.remove(joint)
                break


class Cloth(Framework):
    name = "Cloth"
    description = "(w) Toggle wind"

    def __init__(self):
        super(Cloth, self).__init__()
        self.wind = False
        self.segment_count = (18, 25)
        self.body_size = 0.22

        cloth_info = create_cloth(
            self.world, self.segment_count, self.body_size)
        self.cloth, self.weld_joints, self.dist_joints = cloth_info

    def Keyboard(self, key):
        if key == Keys.K_w:
            self.wind = not self.wind

    def Step(self, settings):
        super(Cloth, self).Step(settings)
        if self.wind:
            self.Print('Wind enabled')
        step_cloth(self.world, self.cloth, self.wind, self.body_size,
                   self.segment_count, self.dist_joints)

if __name__ == "__main__":
    main(Cloth)
