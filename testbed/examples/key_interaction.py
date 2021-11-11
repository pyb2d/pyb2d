import sys, os


from framework import Framework,Testbed
import pybox2d as b2



class KeyInteraction(Framework):
    name = "KeyInteraction"
    description = "This demonstrates how check if a key is pressed"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(KeyInteraction, self).__init__(gui=gui)

        # Ground body
        world = self.world
        ground = world.create_body(
            shapes=b2.edge_shape(vertices=[(-40, 0), (40, 0)])
        )

     
        # Small triangle
        triangle = b2.fixture_def(
            shape=b2.polygon_shape(vertices=[(-1, 0), (1, 0), (0, 2)])
        )
        self.body = world.create_dynamic_body(
            position=(-5, 2),
            fixtures=triangle,
        )

    def pre_step(self, dt):
        
        if self.is_key_down('W'):
            self.body.apply_force_to_center(b2.vec2([0,20]), True)
        if self.is_key_down('A'):
            self.body.apply_force_to_center(b2.vec2([-20,0]), True)
        if self.is_key_down('S'):
            self.body.apply_force_to_center(b2.vec2([0,-20]), True)
        if self.is_key_down('D'):
            self.body.apply_force_to_center(b2.vec2([20,0]), True)

        

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(KeyInteraction)
    testbed.run()
