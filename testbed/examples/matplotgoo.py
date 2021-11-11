import sys, os

from pybox2d.framework import Framework,Testbed
from pybox2d import *



import pybox2d
import logging
from pybox2d import JointType





def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)



class MatplotlibDebugDraw(pybox2d.DebugDraw):
    def __init__(self, canvas):
        super(MatplotlibDebugDraw,self).__init__(float_colors=False)



        #self.ppm = ppm
        #self.ippm = 1.0 / self.ppm
        self.outline_width = 0.01
        self.segment_width = 0.01
        self._bounding_box = [ [0,0],[0,0]]

        self.joint_colors = {
            JointType.unknown_joint :   (230, 25, 75),
            JointType.revolute_joint :  (255,0, 0),
            JointType.prismatic_joint : (255, 225, 25),
            JointType.distance_joint :  (0, 130, 200),
            JointType.pulley_joint :    (245, 130, 48),
            JointType.mouse_joint :     (145, 30, 180),
            JointType.gear_joint :      (70, 240, 240),
            JointType.wheel_joint :     (240, 50, 230),
            JointType.weld_joint :      (210, 245, 60),
            JointType.friction_joint :  (250, 190, 190),
            # JointType.rope_joint :      (0, 128, 128),
            JointType.motor_joint :     (230, 190, 255),
        }

    def set_painter(self, painter, option, widget):
        self.painter = painter
        self.option = option
        self.widget = widget

    def reset_bounding_box(self):
        self._bounding_box = [ [0,0],[0,0]]

    def _update_bounding_box(self, p):
        for c in range(2):
            if p[c] < self._bounding_box[0][c]:
                self._bounding_box[0][c] = p[c]

            if p[c] > self._bounding_box[1][c]:
                self._bounding_box[1][c] = p[c]

    def draw_solid_circle(self, center, radius, axis, color):

        pass
                
    def draw_circle(self, center, radius, color):


        pass

    def draw_segment(self,v1, v2, color):


        pass
            
    def draw_polygon(self,vertices, color):


        pass

    def draw_solid_polygon(self,vertices, color):
        pass

    def draw_particles(self, centers, radius, colors=None):
        pass

    def draw_joint(self, joint):
        
        pass





class MatplotlibTestbedGui(object):
    def __init__(self, testbed):
        self.testbed = testbed
        

    def run(self):
        app = QtGui.QApplication([])
        vbw = PgFrameworkWidget(testbed=self.testbed)
        vbw.show()
        QtGui.QApplication.instance().exec_()





class Web(Framework):
    name = "Web"
    description = "goo"
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
        fixture = fixture_def(shape=circle_shape(radius=1),
                               density=5, friction=0.9)
        print('cc')

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

    testbed = Testbed(guiType=MatplotlibTestbedGui)
    testbed.setExample(Web)
    testbed.run()
