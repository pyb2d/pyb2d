import sys, os
from pybox2d.framework import Framework,Testbed
from pybox2d import *



class DamnBreak(Framework):
    name = "DamnBreak"
    description = "This demonstrates a soft distance joint. Press: (b) to delete a body, (j) to delete a joint"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(DamnBreak, self).__init__(gui=gui)

        verts=[
            b2Vec2(-2, 0),
            b2Vec2(4, 0),
            b2Vec2(4, 8),
            b2Vec2(-2, 8)
        ]
        groundbody = self.world.create_static_body(
            shapes=loop_shape(vertices=verts)
        )



        fixtureA = fixture_def(shape=circle_shape(0.5),density=2.2, friction=0.2)
        body = self.world.create_dynamic_body(
            #bodyDef = bodyDef(linearDamping=2.0,angularDamping=2.0),                                              
            position=(1,2.5),
            fixtures=fixtureA
        ) 


        pdef = particle_system_def(viscous_strength=5.0,spring_strength=0.0)
        psystem = self.world.create_particle_system(pdef)
        psystem.radius = 0.045
        psystem.damping = 0.2


        shape = polygon_shape(box=(2.0,2.0),center=vec2(0,2.01),angle=0)
        pgDef = particle_group_def(flags=ParticleFlag.waterParticle, 
                                 group_flags=ParticleGroupFlag.solidParticleGroup,
                                 shape=shape,strength=0.0
                                 )

        group = psystem.create_particle_group(pgDef)



       

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(DamnBreak)
    testbed.run()

    #main(DamnBreak)
