from b2d.testbed import TestbedBase
import b2d

class NewtonsCradle(TestbedBase):

    name = "newton's cradle"
    
    def __init__(self): 
        super(NewtonsCradle, self).__init__()
    
        # radius of the circles
        r  = 1.0 
        # length of the rope
        l  = 30.0
        # how many balls
        n  =20

        offset = (0,0)
        dynamic_circles = []
        static_bodies = []
        for i in range(n):
            circle = self.world.create_dynamic_body(
                position = (offset[0] +  i*2*r, offset[1]),
                fixtures=b2d.fixture_def(
                    shape=b2d.circle_shape(radius=r*0.99),
                    density=1.0,
                    restitution=1.0,
                    friction=0.0
                ),
                linear_damping=0.01,
                angular_damping=1.0,
                fixed_rotation=True
            ) 
            dynamic_circles.append(circle)

            static_body = self.world.create_static_body(
                position = (offset[0] + i*2*r, offset[1] + l)
            ) 

            self.world.create_distance_joint(static_body, circle,
                local_anchor_a=(0,0),
                local_anchor_b=(0,0),
                max_length=l,
                stiffness=0,
            )

            static_bodies.append(static_body)
        
if __name__ == "__main__":
    from b2d.testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 40,
        "resolution" : (1000,1000)
    }
    NewtonsCradle.run(PygameGui, gui_settings=gui_settings)