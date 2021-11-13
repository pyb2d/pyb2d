from testbed import TestbedBase
import random
import numpy
import pybox2d as b2

class FuncShape(TestbedBase):

    name = "the func shape"
    
    def __init__(self): 
        super(FuncShape, self).__init__()
 

        
        x = numpy.linspace(start=1,stop=100, num=500)
        y = numpy.sin(x) * numpy.log(x)
        verts = numpy.stack([x,y],-1)
        verts = numpy.require(verts, requirements=['C'])

        # print("verts",verts.shape)
        # verts = [b2.b2Vec2(x,y) for x,y in verts]
        shape =  b2.chain_shape(
            vertices=numpy.flip(verts,axis=0)
        )

        box = self.world.create_static_body( position=(0, 0), shape = shape)

        for i in range(30):
            box = self.world.create_dynamic_body(
                position=(10+random.random()*10,random.random()*10 + 10),
                shape=b2.circle_shape(pos=(0,0), radius=0.7),
                density=1.0,
            )




if __name__ == "__main__":
    from testbed.backend.pygame import PygameGui
    gui_settings = {
        "fps" : 40,
        "resolution" : (1000,1000)
    }
    FuncShape.run(PygameGui, gui_settings=gui_settings)