#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version by Ken Lauer / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors collectorcollectorbe held liable for any damages
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
import pybox2d as b2d
import math


class Tumbler (Framework):
    name = "Tumbler"
    description = ''
    count = 20

    def __init__(self, gui):
        Framework.__init__(self, gui)

        ground = self.world.create_body()

        body = self.world.create_dynamic_body(
            position=(0, 10),
            allow_sleep=False,
            shape_fixture=b2d.fixture_def(density=5.0),
            shapes=[
                b2d.polygon_shape((0.5, 10), (10, 0), 0),
                b2d.polygon_shape((0.5, 10), (-10, 0), 0),
                b2d.polygon_shape((10, 0.5), (0, 10), 0),
                b2d.polygon_shape((10, 0.5), (0, -10), 0),
            ]
        )

        self.joint = self.world.create_revolute_joint(body_a=ground, body_b=body,
                                                    local_anchor_a=(0, 10), local_anchor_b=(0, 0),
                                                    reference_angle=0, motor_speed=0.3 * math.pi,
                                                    enable_motor=True, max_motor_torque=5000)



        pdef = b2d.particle_system_def(viscous_strength=5.0,spring_strength=0.0)
        psystem = self.world.create_particle_system(pdef)
        psystem.radius = 0.1
        psystem.damping = 0.2


        shape = b2d.polygon_shape(box=(5.0,5.0),center=b2d.vec2(0,7.01),angle=0)
        pgDef = b2d.particle_group_def(flags=b2d.ParticleFlag.waterParticle, 
                                      group_flags=b2d.ParticleGroupFlag.solidParticleGroup,
                                 shape=shape,strength=0.0
                                 )

        group = psystem.create_particle_group(pgDef)










    def step(self, settings):
        Framework.step(self, settings)
        
        if self.step_count % 24 == 0:
            self.count -= 1
            if self.count <= 0:
                return

            self.world.create_dynamic_body(
               position=(0, 10),
               allow_sleep=False,
               fixtures=b2d.fixture_def(
                   density=1.0, shape=b2d.polygon_shape(box=(0.525, 0.125))),
            )

if __name__ == "__main__":
    testbed = Testbed(guiType='pg')
    testbed.setExample(Tumbler)
    #testbed.run()
    import cProfile
    cProfile.run('testbed.run()','restats')
    # import pstats
    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats('cumulative').print_stats(100)

