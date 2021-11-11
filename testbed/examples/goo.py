import sys, os

from pybox2d.framework import Framework,Testbed
from pybox2d import *

class Web(Framework):
    name = "Web"
    description = "goo"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(Web, self).__init__(gui)

        # The ground
        ground = self.world.create_static_body(
            shapes=edge_shape(vertices=[(-40, 0), ( 40, 0)])
        )
        fixture = fixture_def(shape=circle_shape(radius=1),
                               density=5, friction=0.9)

        self.bodies =[]
        shape = [10, 40]
        for x in range(shape[0]):
            b = []
            for y in range(shape[1]):
                pos = (x*4,y*4 +1 )
                b.append(self.world.create_dynamic_body(position=pos,fixtures=fixture, angular_damping=10.5, linear_damping=0.5))
            self.bodies.append(b)
    #     bodies = self.bodies

        # We will define the positions in the local body coordinates, the length
        # will automatically be set by the __init__ of the b2DistanceJointDef


        self.joints = []
        def connect(body_a, body_b):
            stiffness, damping = linear_stiffness(frequency_hz=5.0, damping_ratio=0.5, body_a=body_a, body_b=body_b)
            dfn = distance_joint_def(
                stiffness=stiffness,
                damping=damping,
                body_a=body_a,
                body_b=body_b,
                # local_anchor_a=local_anchor_a,
                # local_anchor_b=local_anchor_b
            )
            self.joints.append(self.world.create_joint(dfn))

        for x in range(shape[0]):
            for y in range(shape[1]):

                if x+1 < shape[0]:
                    connect(self.bodies[x][y], self.bodies[x+1][y])
                if y+1 < shape[1]:
                    connect(self.bodies[x][y], self.bodies[x][y+1])

                if x+1 < shape[0] and y+1 < shape[1]:
                    connect(self.bodies[x][y], self.bodies[x+1][y+1])

                if x-1 >= 0 and y+1 < shape[1]:
                    connect(self.bodies[x][y], self.bodies[x-1][y+1])
                
                
    # # def Keyboard(self, key):
    #     if key == Keys.K_b:
    #         for body in self.bodies:
    #             # Gets both FixtureDestroyed and JointDestroyed callbacks.
    #             self.world.destroyBody(body)
    #             break

    #     elif key == Keys.K_j:
    #         for joint in self.joints:
    #             # Does not get a JointDestroyed callback!
    #             self.world.destroyJoint(joint)
    #             self.joints.remove(joint)
    #             break

    # def FixtureDestroyed(self, fixture):
    #     super(Web, self).FixtureDestroyed(fixture)
    #     body = fixture.body
    #     if body in self.bodies:
    #         print(body)
    #         self.bodies.remove(body)
    #         print("Fixture destroyed, removing its body from the list. Bodies left: %d"
    #               % len(self.bodies))

    # def JointDestroyed(self, joint):
    #     if joint in self.joints:
    #         self.joints.remove(joint)
    #         print("Joint destroyed and removed from the list. Joints left: %d"
    #               % len(self.joints))

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(Web)
    testbed.run()
