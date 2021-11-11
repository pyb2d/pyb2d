import sys, os


from framework import Framework,Testbed
import pybox2d as b2



class KeyInteractionAdvanced(Framework):
    name = "KeyInteractionAdvanced"
    description = "This demonstrates how  use keyboard interaction"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(KeyInteractionAdvanced, self).__init__(gui=gui)

        # Ground body
        world = self.world
        ground = world.create_body(
            shapes=b2.edge_shape(vertices=[(-40, 0), (40, 0)])
        )
        
        children = [
            {'name': 'Integer', 'type': 'int', 'value': 10},
            {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
            {'name': 'Subgroup', 'type': 'group', 'children': [
                {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
                {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
            ]}
        ]

        param = gui.add_param(name='Group', type='group', children=children)
        print('theparam',param)
        print('theparam',gui.get_param_value('Group'))


        param = gui.add_param(name='Integer', type='int', value=10)
        print('Integer',param)
        print('Integer',gui.get_param_value('Integer'))
        # Small triangle
        triangle = b2.fixture_def(
            shape=b2.polygon_shape(vertices=[(-1, 0), (1, 0), (0, 2)])
        )
        self.body = world.create_dynamic_body(
            position=(-5, 2),
            fixtures=triangle,
        )

    def on_key_down(self, key):
        if key == "G":
            self.body.gravity_scale = 0.0


    def on_key_up(self, key):
        if key == "G":
            self.body.gravity_scale = 1.0

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
    testbed.setExample(KeyInteractionAdvanced)
    testbed.run()
