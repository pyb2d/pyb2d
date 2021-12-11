"""
Function Shape
===========================

This example show how to create a shape from a mathematical function.
In this example we use f(x) = sin(x) + log(x) + 5.5
"""

from b2d.testbed import TestbedBase
import random
import numpy
import b2d 

class FunctionShape(TestbedBase):

    name = "Function Shape"
    
    def __init__(self, settings=None): 
        super(FunctionShape, self).__init__(settings=settings)
   
        x = numpy.linspace(start=1,stop=30, num=100)
        y = numpy.sin(x) * numpy.log(x) + 5.5
        verts = numpy.stack([x,y],-1)
        verts = numpy.require(verts, requirements=['C'])

        shape =  b2d.chain_shape(
            vertices=numpy.flip(verts,axis=0)
        )

        box = self.world.create_static_body( position=(0, 0), shape = shape)

        for i in range(30):
            box = self.world.create_dynamic_body(
                position=(10+random.random()*10,random.random()*10 + 10),
                shape=b2d.circle_shape(pos=(0,0), radius=0.7),
                density=1.0,
            )


if __name__ == "__main__":
        
    ani = b2d.testbed.run(FunctionShape)
    ani