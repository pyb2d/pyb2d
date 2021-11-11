from testbed import TestbedBase
import random
import numpy
import pybox2d as b2

class GaussMachine(TestbedBase):

    name = "the func shape"
    
    def __init__(self): 
        super(GaussMachine, self).__init__()
 
        self.box_shape= 80,20
        box_shape = self.box_shape
            
        #  outer box
        verts =numpy.array([
            (0, box_shape[1]),(0,0),(box_shape[0],0), (box_shape[0], box_shape[1])
        ])
        shape =  b2.chain_shape(
            vertices=numpy.flip(verts,axis=0)
        )
        box = self.world.create_static_body( position=(0, 0), shape = shape)

        # "bins"
        bin_height = box_shape[1] / 3
        bin_width = 1
        for x in range(0,box_shape[0], bin_width):

            shape = b2.EdgeShape()
            shape.set_two_sided((x, 0), (x,bin_height))
            box = self.world.create_static_body( position=(0, 0), shape =shape)

        # reflectors
        ref_start_y = int(bin_height + box_shape[1]/10.0)
        ref_stop_y = int(box_shape[1]*0.9)
        print(ref_start_y)
        for x in range(0, box_shape[0]+1):
            
            for y in range(ref_start_y, ref_stop_y):
                s = [0.5,0][y % 2 == 0]
                shape = b2.circle_shape(radius=0.3)
                box = self.world.create_static_body( position=(x+s, y), shape =shape)

    def pre_step(self, dt):
        for x in range(3):
            box = self.world.create_dynamic_body(
                    position=(self.box_shape[0]/2+random.random()*0.4-0.25, self.box_shape[1]),
                    shape=b2.circle_shape(pos=(0,0), radius=0.1),
                    density=1.0,
                )


if __name__ == "__main__":
    from testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 40,
        "resolution" : (1000,1000)
    }
    GaussMachine.run(PygameGui, gui_settings=gui_settings)