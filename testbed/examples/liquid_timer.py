import sys, os
sys.path.append('../')
sys.path.append("/home/ciclon/bld/liquidfun/liquidfun/Box2D/python")
from framework import Framework,Testbed
from pybox2d import *

import pybox2d as b2


class LiquidTimer(Framework):
    name = "LiquidTimer"
    description = ""
    bodies = []
    joints = []

    def __init__(self, gui):
        super(LiquidTimer, self).__init__(gui=gui)


        world = self.world

        #pdef = b2.particleSystemDef(viscousStrength=5.0,springStrength=0.0)
        pdef = b2.particle_system_def(viscous_strength=2)
        psystem = world.create_particle_system(pdef)


        # ground body
        groud = world.create_static_body(shape=b2.chain_shape(
            vertices=[(-2, 0), (2, 0), (2, 4), (-2, 4)],
            loop=True
        ))


        psystem.radius = 0.125
        shape = b2.polygon_shape(box=(2,0.4),center=(0,3.6))
        pgd = b2.particle_group_def(shape=shape,lifetime=2,
                                  flags=ParticleFlag.viscousParticle)
        psystem.create_particle_group(pgd)


        # edge shaped bodies
        edgeShapesVerts = [
            [(-2, 3.2), (-1.2, 3.2) ],
            [(-1.1, 3.2), (2, 3.2)],
            [(-1.2, 3.2), (-1.2, 2.8)],
            [(-1.1, 3.2), (-1.1, 2.8)],
            [(-1.6, 2.4), (0.8, 2)],
            [(1.6, 1.6), (-0.8, 1.2)],
            [(-1.2, 0.8), (-1.2, 0)],
            [(-0.4, 0.8), (-0.4, 0)],
            [(0.4, 0.8), (0.4, 0)],
            [(1.2, 0.8), (1.2, 0)]
        ]
        for verts in edgeShapesVerts:
            body = world.create_static_body(shape=b2.edge_shape(
                vertices=verts
            ))


if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(LiquidTimer)
    testbed.run()
