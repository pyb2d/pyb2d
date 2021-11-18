from testbed import TestbedBase
import random
import numpy
import b2d as b2




class AngryCircles(TestbedBase):

    name = "the func shape"
    
    def __init__(self): 
        super(AngryCircles, self).__init__()
    


        dimensions = [100,50]
        
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

        # the catapult
        p0 = self.world.create_static_body( position=(20, 30), shape = b2.circle_shape( radius=0.2))
        p1 = self.world.create_static_body( position=(30, 30), shape = b2.circle_shape( radius=0.2))

        shuffle = self.world.create_dynamic_body(position=(20,20), shapes=[
            b2.polygon_shape(box=[0.3,2], center=[0.05,1]),
            b2.polygon_shape(box=[2,0.3], center=[1,0])
        ], density=1.0)


        # joints holding the "shuffle"
        stiffness, damping = b2.linear_stiffness(frequency_hz=2.0, damping_ratio=0.5, body_a=shuffle, body_b=p0)
        dfn = self.world.create_joint( b2.distance_joint_def(
            stiffness=stiffness,
            damping=damping,
            body_a=shuffle,
            body_b=p0,
            local_anchor_a=(0,3),
            length=5
            # local_anchor_b=local_anchor_b
        ))

        stiffness, damping = b2.linear_stiffness(frequency_hz=2.0, damping_ratio=0.5, body_a=shuffle, body_b=p1)
        dfn = self.world.create_joint( b2.distance_joint_def(
            stiffness=stiffness,
            damping=damping,
            body_a=shuffle,
            body_b=p1,
            local_anchor_a=(3,0),
            length=5
            # local_anchor_b=local_anchor_b
        ))


        # amo
        box = self.world.create_dynamic_body(
                position=(0,1),
                shape=b2.circle_shape(pos=(0,0), radius=0.8),
                density=0.2,
            )

        # targets
        p0 = self.world.create_static_body( position=(40, 30), shape = b2.edge_shape( [(0, 0), (20,0)] ))    

        for i in range(10):

            self.world.create_dynamic_body(position=(40+i+1,32), shapes=[
            b2.polygon_shape(box=[0.2,2], center=[0,0])
        ], density=1.0)


if __name__ == "__main__":
    from testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 40,
        "resolution" : (1000,1000)
    }
    AngryCircles.run(PygameGui, gui_settings=gui_settings)