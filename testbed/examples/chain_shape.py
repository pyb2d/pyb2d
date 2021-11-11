from pybox2d.framework import Framework,Testbed

from bridge import create_bridge
import math
from math import sqrt
import random
import pybox2d as b2


class ChainShape (Framework):
    name = "ChainShape"
    description = "Keys: left = a, brake = s, right = d, hz down = q, hz up = e"
    hz = 20
    zeta = 0.7
    speed = 50
    bridgePlanks = 20



    def __init__(self, gui):
        super(ChainShape, self).__init__(gui)
        self.box_shape = (10,20)
        verts = [
            b2.b2Vec2(0,0),
            b2.b2Vec2(0,self.box_shape[1]),
            b2.b2Vec2(self.box_shape[0],self.box_shape[1]),
            b2.b2Vec2(self.box_shape[0],0),
            b2.b2Vec2(0,0),
        ]

        box = self.world.create_static_body(
            position=(0, 0),
            fixtures=b2.fixture_def(
                shape=b2.chain_shape(
                    vertices=verts, 
                    prev_vertex=verts[0], 
                    next_vertex=verts[-1]
                ),
                density=1.0,
            )
        )


        for i in range(7):


            box = self.world.create_dynamic_body(
                position=(0, 0),
                fixtures=b2.fixture_def(
                    shape=b2.circle_shape(pos=(random.random()*self.box_shape[0],random.random()*self.box_shape[1]), radius=0.7),
                    density=1.0,
                )
            )


if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(ChainShape)
    testbed.run()

