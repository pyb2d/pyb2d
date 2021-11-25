"""
Blender
===========================

This example show how to create a blender with Box2D
"""


from b2d.testbed import TestbedBase
import random
import numpy
import b2d

class Blender(TestbedBase):

    name = "blender"
    
    def __init__(self): 
        super(Blender, self).__init__()
        dimensions = [30,30]
        
        # the outer box
        box_shape = b2d.ChainShape()
        box_shape.create_loop([
                (0,0),
                (0,dimensions[1]),
                (dimensions[0],dimensions[1]),
                (dimensions[0],0)
            ]
        )
        box = self.world.create_static_body( position=(0, 0), 
            fixtures=b2d.fixture_def(
                shape = box_shape,
                friction=0
            )
        )


        for i in range(20):
            circle = self.world.create_dynamic_body(
                    position=(dimensions[0]/2 + random.random(), 1 + random.random()), 
                    fixtures=b2d.fixture_def(
                        density=1.0,
                        shape=b2d.circle_shape(radius=1.0),
                        restitution=1
                    ),
                    angular_damping=0,
                    linear_damping=0)



        body_a = self.world.create_static_body(
            position=(dimensions[0]/2, dimensions[1]/2), 
        )
        l = 7.2
        body_b = self.world.create_dynamic_body(
                position=(dimensions[0]/2, dimensions[1]/2), 
                shape=b2d.polygon_shape(box=[0.4, l]),
                density=1,
                angular_damping=0,
                linear_damping=0)

        joint = self.world.create_revolute_joint(
            body_a=body_a,
            body_b=body_b,
            local_anchor_a=(0, 0),
            local_anchor_b=(0, l),
            collide_connected=False,
            enable_motor=True,
            max_motor_torque=100000,
            motor_speed=3
        )



if __name__ == "__main__":

    ani =  b2d.testbed.run(Blender)
    ani