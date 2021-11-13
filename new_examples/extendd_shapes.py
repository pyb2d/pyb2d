from testbed import TestbedBase
import random
import numpy
import pybox2d as b2
import math



# 8 bit segment

def char_to_shapes(c):
    if c in ['o','O']:
        return [b2.circle_shape(radius=1)]
    elif c in ['q','Q']:
        # return [
        #     b2.circle_shape(radius=1),
        #     b2.polygon_shape(box=[0.5,0.25], center=(1,-0.5))
        # ]

        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,-0.75)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,0.75)),
            b2.polygon_shape(box=[0.25,1], center=(1,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(1,-0.75))
        ]


    elif c in ['h','H']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,0)),
            b2.polygon_shape(box=[0.25,1], center=(1,0))
        ]

    elif c in ['u','U']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,-0.75)),
            b2.polygon_shape(box=[0.25,1], center=(1,0))
        ]

    elif c in ['a','A']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,0.75)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.25,-0.19)),
            b2.polygon_shape(box=[0.25,1], center=(1,0))
        ]
    elif c in ['n','N']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.25,0.98], center=(0.5,0), angle=math.pi*1.1/8.0),
            b2.polygon_shape(box=[0.25,1], center=(1,0))
        ]

    elif c in ['t','T']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0.5,0)),
            b2.polygon_shape(box=[0.75,0.25], center=(0.5,0.75)),
        ]

    elif c in ['s','S']:
        return [
            b2.polygon_shape(box=[0.75,0.25], center=(0.5,0.75)),
            b2.polygon_shape(box=[0.25,0.25], center=(0.0,0.5)),
            b2.polygon_shape(box=[0.75,0.25], center=(0.5,0.0)),
            b2.polygon_shape(box=[0.25,0.25], center=(1,-0.5)),
            b2.polygon_shape(box=[0.75,0.25], center=(0.5,-0.75))
        ]
    elif c in ['c','C']:
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.5,-0.75)),
            b2.polygon_shape(box=[0.5,0.25], center=(0.5, 0.75)),
        ]
    elif c in ['k','K']:
        angle = math.pi*1.2/8.0
        return [
            b2.polygon_shape(box=[0.25,1], center=(0,0)),
            b2.polygon_shape(box=[0.25,0.55], center=(0.5,-0.4), angle=angle),
            b2.polygon_shape(box=[0.25,0.55], center=(0.5, 0.4), angle=-angle),
        ]





# vert UNIT shapes


def ngong(n):
    pass

# x is fixed to be 1
def rectangle(y_size):
    pass











class Example(TestbedBase):

    name = "the func shape"
    
    def __init__(self): 
        super(Example, self).__init__()
    


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

        for i,c in enumerate("QUANTSTACK"):
            c = self.world.create_dynamic_body( position=(5+2*i, 2), shapes = char_to_shapes(c), density=1.0, linear_damping=1.0)
if __name__ == "__main__":
    from testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 40,
        "resolution" : (1000,1000)
    }
    Example.run(PygameGui, gui_settings=gui_settings)