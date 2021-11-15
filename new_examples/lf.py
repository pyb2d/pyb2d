from testbed import TestbedBase
import random
import numpy
import pybox2d as b2




class LiquidFun(TestbedBase):

    name = "the func shape"
    
    def __init__(self): 
        super(LiquidFun, self).__init__()
    



        dimensions = [10,10]
        
        # the outer box
        box_shape = b2.ChainShape()
        box_shape.create_loop([
                (0,0),
                (0,dimensions[1]),
                (dimensions[0],dimensions[1]),
                (dimensions[0],0)
            ]
        )
        box = self.world.create_static_body( position=(0, 0), shape = box_shape)




        fixtureA = b2.fixture_def(shape=b2.circle_shape(0.5),density=2.2, friction=0.2, restitution=0.5)
        body = self.world.create_dynamic_body(
            #bodyDef = bodyDef(linearDamping=2.0,angularDamping=2.0),                                              
            position=(1,2.5),
            fixtures=fixtureA
        ) 
# 

        pdef = b2.particle_system_def(viscous_strength=0.2,spring_strength=0.0, damping_strength=2.0)
        psystem = self.world.create_particle_system(pdef)
        psystem.radius = 0.08
        psystem.damping = 1.2


        shape = b2.polygon_shape(box=(10/2,10/2),center=(5,5),angle=0)
        pgDef = b2.particle_group_def(flags=b2.ParticleFlag.viscousParticle, 
                                 group_flags=b2.ParticleGroupFlag.solidParticleGroup,
                                 shape=shape,strength=0.0
                                 )

        group = psystem.create_particle_group(pgDef)





if __name__ == "__main__":
    from testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 30,
        "resolution" : (1000,1000)
    }
    LiquidFun.run(PygameGui, gui_settings=gui_settings)