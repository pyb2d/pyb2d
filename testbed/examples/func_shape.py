from pybox2d.framework import Framework,Testbed

from bridge import create_bridge
import math
from math import sqrt
import random
import pybox2d as b2
import numpy



class FuncShape(Framework):
    name = "FuncShape"
    description = ""




    def __init__(self, gui):
        super(FuncShape, self).__init__(gui)
 

        
        x = numpy.linspace(start=1,stop=100, num=500)
        y = numpy.sin(x) * numpy.log(x)
        verts = numpy.stack([x,y],-1)
        verts = numpy.require(verts, requirements=['C'])

        # print("verts",verts.shape)
        # verts = [b2.b2Vec2(x,y) for x,y in verts]
        shape =  b2.chain_shape(
            vertices=numpy.flip(verts,axis=0), 
            prev_vertex=(float(verts[0,0]),float(verts[0,1])),
            next_vertex=(float(verts[-1,0]),float(verts[-1,1])),
        )

        box = self.world.create_static_body( position=(0, 0), shape = shape)

        for i in range(7):
            box = self.world.create_dynamic_body(
                position=(10+random.random()*10,random.random()*10 + 10),
                shape=b2.circle_shape(pos=(0,0), radius=0.7),
                density=1.0,
            )



if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(FuncShape)
    testbed.run()

