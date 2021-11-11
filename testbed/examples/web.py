import sys, os

from pybox2d.framework import Framework,Testbed
from pybox2d import *

print("AAAA")

class Web(Framework):
    name = "Web"
    description = "This demonstrates a soft distance joint. Press: (b) to delete a body, (j) to delete a joint"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(Web, self).__init__(gui)

        print('acc')
        # The ground
        ground = self.world.create_static_body(
            shapes=edge_shape(vertices=[(-40, 0), ( 40, 0)])
        )
        print('b')
        fixture = fixture_def(shape=polygon_shape(box=(0.5, 0.5)),
                               density=5, friction=0.2)
        print('cc')

        self.bodies =[]
        for pos in ((0-5, 5+2.5), (2.5+5, 5+2.5), (2.5+5, 15+2.5), (2.5-5, 15+2.5)):
            print('acc')
            b = self.world.create_dynamic_body(position=pos,fixtures=fixture)
            print('abb')
            self.bodies.append(b)
        print('c')
        bodies = self.bodies


        # Create the joints between each of the bodies and also the ground
        #         body_a      body_b   local_anchor_a local_anchor_b
        sets = [(ground,    bodies[0], (-10, 0),   (-0.5, -0.5)),
                (ground,    bodies[1], (10, 0),    (0.5, -0.5)),
                (ground,    bodies[2], (10, 20),   (0.5, 0.5)),
                (ground,    bodies[3], (-10, 20),  (-0.5, 0.5)),
                (bodies[0], bodies[1], (0.5, 0),   (-0.5, 0)),
                (bodies[1], bodies[2], (0, 0.5),   (0, -0.5)),
                (bodies[2], bodies[3], (-0.5, 0),  (0.5, 0)),
                (bodies[3], bodies[0], (0, -0.5),  (0, 0.5)),
                ]
        print('d')
        #for b in self.bodies:
        #    print b.GetUserData()

        # We will define the positions in the local body coordinates, the length
        # will automatically be set by the __init__ of the b2DistanceJointDef
        self.joints = []
        for body_a, body_b, local_anchor_a, local_anchor_b in sets:

            stiffness, damping = linear_stiffness(frequency_hz=1.0, damping_ratio=2.1, body_a=body_a, body_b=body_b)
            dfn = distance_joint_def(
                stiffness=stiffness,
                damping=damping,
                body_a=body_a,
                body_b=body_b,
                local_anchor_a=local_anchor_a,
                local_anchor_b=local_anchor_b
            )
            self.joints.append(self.world.create_joint(dfn))

    def Keyboard(self, key):
        if key == Keys.K_b:
            for body in self.bodies:
                # Gets both FixtureDestroyed and JointDestroyed callbacks.
                self.world.destroyBody(body)
                break

        elif key == Keys.K_j:
            for joint in self.joints:
                # Does not get a JointDestroyed callback!
                self.world.destroyJoint(joint)
                self.joints.remove(joint)
                break

    def FixtureDestroyed(self, fixture):
        super(Web, self).FixtureDestroyed(fixture)
        body = fixture.body
        if body in self.bodies:
            print(body)
            self.bodies.remove(body)
            print("Fixture destroyed, removing its body from the list. Bodies left: %d"
                  % len(self.bodies))

    def JointDestroyed(self, joint):
        if joint in self.joints:
            self.joints.remove(joint)
            print("Joint destroyed and removed from the list. Joints left: %d"
                  % len(self.joints))

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(Web)
    testbed.run()
