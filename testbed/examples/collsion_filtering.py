import sys, os


from pybox2d.framework import Framework,Testbed
import pybox2d as b2



class CollisionFiltering(Framework):
    name = "CollisionFiltering"
    description = "This demonstrates a soft distance joint. Press: (b) to delete a body, (j) to delete a joint"
    bodies = []
    joints = []

    def __init__(self, gui):
        super(CollisionFiltering, self).__init__(gui=gui)

        # Ground body
        world = self.world
        ground = world.create_body(
            shapes=b2.edge_shape(vertices=[(-40, 0), (40, 0)])
        )

        # Define the groups that fixtures can fall into
        # Note that negative groups never collide with other negative ones.
        smallGroup = 1
        largeGroup = -1

        # And the categories
        # Note that these are bit-locations, and as such are written in
        # hexadecimal.
        # defaultCategory = 0x0001
        triangleCategory = 0x0002
        boxCategory = 0x0004
        circleCategory = 0x0008

        # And the masks that define which can hit one another
        # A mask of 0xFFFF means that it will collide with everything else in
        # its group. The box mask below uses an exclusive OR (XOR) which in
        # effect toggles the triangleCategory bit, making boxMask = 0xFFFD.
        # Such a mask means that boxes never collide with triangles.  (if
        # you're still confused, see the implementation details below)

        triangleMask = 0xFFFF
        boxMask = 0xFFFF ^ triangleCategory
        circleMask = 0xFFFF

        # The actual implementation determining whether or not two objects
        # collide is defined in the C++ source code, but it can be overridden
        # in Python (with b2ContactFilter).
        # The default behavior goes like this:
        #   if (filterA.group_index == filterB.group_index and filterA.group_index != 0):
        #       collide if filterA.group_index is greater than zero (negative groups never collide)
        #   else:
        #       collide if (filterA.mask_bits & filterB.category_bits) != 0 and (filterA.category_bits & filterB.mask_bits) != 0
        #
        # So, if they have the same group index (and that index isn't the
        # default 0), then they collide if the group index is > 0 (since
        # negative groups never collide)
        # (Note that a body with the default filter settings will always
        # collide with everything else.)
        # If their group indices differ, then only if their bitwise-ANDed
        # category and mask bits match up do they collide.
        #
        # For more help, some basics of bit masks might help:
        # -> http://en.wikipedia.org/wiki/Mask_%28computing%29

        # Small triangle
        triangle = b2.fixture_def(
            shape=b2.polygon_shape(vertices=[(-1, 0), (1, 0), (0, 2)]),
            density=1,
            shape_filter=b2.shape_filter(
                group_index=smallGroup,
                category_bits=triangleCategory,
                mask_bits=triangleMask,
            )
        )
        world.create_dynamic_body(
            position=(-5, 2),
            fixtures=triangle,
        )


        # ?!?!?!?!
        # triangle.shape.vertices = [
        #     b2.vec2(v) *2.0 for v in triangle.shape.vertices]
        
        triangle.filter.group_index = largeGroup

        trianglebody = world.create_dynamic_body(
            position=(-5, 6),
            fixtures=triangle,
            fixed_rotation=True,  # <--
        )
        # note that the large triangle will not rotate
        
        # Small box
        box = b2.fixture_def(
            shape=b2.polygon_shape(box=(1, 0.5)),
            density=1,
            restitution=0.1,
            shape_filter = b2.shape_filter(
                group_index=smallGroup,
                category_bits=boxCategory,
                mask_bits=boxMask,
            )
        )

        world.create_dynamic_body(
            position=(0, 2),
            fixtures=box,
        )

        # Large box
        box.shape  = b2.polygon_shape(box=(1, 0.5))
        box.filter.group_index = largeGroup
        world.create_dynamic_body(
            position=(0, 6),
            fixtures=box,
        )

        # Small circle
        circle = b2.fixture_def(
            shape=b2.circle_shape(radius=1),
            density=1,
            shape_filter=b2.shape_filter(
                group_index=smallGroup,
                category_bits=circleCategory,
                mask_bits=circleMask,
            )
        )

        world.create_dynamic_body(
            position=(5, 2),
            fixtures=circle,
        )

        # Large circle
        circle.shape.radius *= 2
        circle.filter.group_index = largeGroup
        world.create_dynamic_body(
            position=(5, 6),
            fixtures=circle,
        )

        # Create a joint for fun on the big triangle
        # Note that it does not inherit or have anything to do with the
        # filter settings of the attached triangle.
        box = b2.fixture_def(shape=b2.polygon_shape(box=(0.5, 1)), density=1)

        testbody = world.create_dynamic_body(
            position=(-5, 10),
            fixtures=box,
        )
        world.create_distance_joint(
            body_a=trianglebody,
            body_b=testbody,
            stiffness=1.0,
            damping=2.1,
            #enable_limit=True,
            #local_anchor_a=(0, 4),
            local_anchor_b=(0, 0),
            #local_axis_a=(0, 1),
            #lower_translation=-1,
           # upper_translation=1,
        )

if __name__ == "__main__":

    testbed = Testbed(guiType='pg')
    testbed.setExample(CollisionFiltering)
    testbed.run()
