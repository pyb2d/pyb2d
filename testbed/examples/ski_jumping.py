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
        
        self.create_slope()
        

        for i in range(1):
            box = self.world.create_dynamic_body(
                position=(0, self.slope_f(0)+1),
                shape=b2.circle_shape(pos=(0,0), radius=1.7),
                density=1.0,
            )

    def slope_f(self, x):
        return (0.1*(x-100))**2

    def create_slope(self):

        # the slope
        x = numpy.linspace(start=-10,stop=130, num=500)
        y = self.slope_f(x)
        verts = numpy.stack([x,y],-1)
        verts = numpy.require(verts, requirements=['C'])

        shape =  b2.chain_shape(
            vertices=numpy.flip(verts,axis=0), 
            prev_vertex=(float(verts[0,0]),float(verts[0,1])),
            next_vertex=(float(verts[-1,0]),float(verts[-1,1])),
        )

        box = self.world.create_static_body( position=(0, 0), shape = shape)

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(FuncShape)
    testbed.run()

