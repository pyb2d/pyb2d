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
            position=(0, -8),
            allow_sleep=False,
            shape_fixture=b2d.fixture_def(density=5.0),
            shapes=[
                b2d.polygon_shape((0.5, 10), (10, 0), 0),
                b2d.polygon_shape((0.5, 10), (-10, 0), 0),
                b2d.polygon_shape((10, 0.5), (0, 10), 0),
                b2d.polygon_shape((10, 0.5), (0, -10), 0),
            ]
        )

        pdef = b2d.particle_system_def(viscous_strength=100,spring_strength=0.0)
        self.psystem = self.world.create_particle_system(pdef)
        self.psystem.radius = 0.3
        self.psystem.damping = 0.2


        pgDef = b2d.particle_group_def(flags=b2d.ParticleFlag.waterParticle, 
                                      group_flags=b2d.ParticleGroupFlag.solidParticleGroup,
                                     strength=0.0)

        self.group = self.psystem.create_particle_group(pgDef)






    def step(self, settings):
        Framework.step(self, settings)
        r = random.random()
        px =(random.random() - 0.5)*10.0
        py =(random.random() - 0.5)*2.0

        if self.step_count < 1500:
            pd = b2d.particle_def(group=self.group, position=(px, py))#, velocity=(vx,vy))
            self.psystem.create_particle(pd)


if __name__ == "__main__":
    testbed = Testbed(guiType='pg')
    testbed.setExample(Tumbler)
    testbed.run()
    #import cProfile
    #cProfile.run('testbed.run()','restats')
    # import pstats
    #p = pstats.Stats('restats')
    #p.strip_dirs().sort_stats('cumulative').print_stats(100)

