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
import random

class Tumbler (Framework):
    name = "Tumbler"
    description = ''
    count = 20

    def __init__(self, gui):
        Framework.__init__(self, gui)

        ground = self.world.create_body()

        body = self.world.create_static_body(
            position=(0, -10),
            allow_sleep=False,
            shape_fixture=b2d.fixture_def(density=5.0),
            shapes=[
                b2d.polygon_shape((3, 200), (200, 0), 0),
                b2d.polygon_shape((3, 200), (-200, 0), 0),
                b2d.polygon_shape((200, 3), (0, 200), 0),
                b2d.polygon_shape((200, 3), (0, -200), 0),
            ]
        )

        pdef = b2d.particle_system_def(viscous_strength=10,spring_strength=0.0,
            density=0.1)
        self.psystem = self.world.create_particle_system(pdef)
        self.psystem.radius = 0.2
        self.psystem.damping = 0.2


        empty_group = b2d.particle_group_def(flags=b2d.ParticleFlag.waterParticle, 
                                      group_flags=b2d.ParticleGroupFlag.solidParticleGroup & b2d.ParticleGroupFlag.particleGroupCanBeEmpty,
                                    )

        self.group = self.psystem.create_particle_group(empty_group)




        self.emitter_body = self.world.create_dynamic_body(
            position=(0, 0),
            allow_sleep=False,
            fixtures=b2d.fixture_def(
                density=1.0, 
                shape=b2d.polygon_shape(box=(3, 0.5))
            ),
        )


        if True:
            edef  = b2d.LinearEmitterDef()
            edef.body = self.emitter_body
            edef.transform = b2d.transform((0,0),0)
            edef.size = b2d.vec2(6,1)
            edef.velocity = b2d.vec2(0,1)
            edef.emite_rate = 2000
            edef.lifetime = 1.0
            self.emitter = b2d.LinearEmitter(self.psystem, self.group, edef)
        else:
            edef  = b2d.RadialEmitterDef()
            edef.position = b2d.vec2(3,-3)
            edef.inner_radius = 3.0
            edef.outer_radius = 5.0
            edef.velocity_magnitude = 200.0
            edef.emite_rate = 10
            edef.lifetime = 8.0
            edef.start_angle = 0 + math.pi
            edef.stop_angle = math.pi /4.0 + math.pi
            self.emitter = b2d.RadialEmitter(self.psystem, self.group, edef)

    def post_step(self, dt):
        #Framework.step(self, dt)
        if True:
            lc = list(self.emitter_body.local_center)
            lc[1]  +=1.5
            pos = self.emitter_body.get_world_point(b2d.vec2(lc))
            #print(pos)
            self.emitter.position = b2d.vec2(pos)
            self.emitter.angle = self.emitter_body.angle
            self.emitter.step(dt)



if __name__ == "__main__":
    testbed = Testbed(guiType='pg')
    testbed.setExample(Tumbler)
    testbed.run()
    #import cProfile
    #cProfile.run('testbed.run()','restats')
    # import pstats
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats('cumulative').print_stats(100)

