"""
Distance Joint
===========================

Create distance joints
"""


# %%
# Imports
import b2d
import numpy as np
import b2d.plot
import matplotlib.pyplot as plt


# %%
# Create distance joints between a static anchor
# and a body directly below the anchor.
# We create 10 distance joints with various
# values for the stiffness

world = b2d.world(gravity=(0, -10))

for i in range(10):

    # create static anchor (does not need shape/fixture)
    anchor = world.create_static_body(position=(i, 0))

    # 5 below the anchor
    body = world.create_dynamic_body(
        position=(i, -10),
        fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=0.4), density=0.5),
    )

    # distance joints of various stiffness-es
    world.create_distance_joint(anchor, body, length=10, stiffness=0.5 * (i + 1))

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10), t=5)
ani
plt.title("increasing stiffness from left to right")
plt.show()


# %%
# Here we vary the damping of the distance joint

world = b2d.world(gravity=(0, -10))

for i in range(10):

    # create static anchor (does not need shape/fixture)
    anchor = world.create_static_body(position=(i, 0))

    # 5 below the anchor
    body = world.create_dynamic_body(
        position=(i, -10),
        fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=0.4), density=0.5),
    )

    # distance joints of various stiffness-es
    world.create_distance_joint(anchor, body, length=10, stiffness=2, damping=0.05 * i)

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10), t=5)
ani
plt.title("increasing damping from left to right")
plt.show()


# %%
# Distance joints can be used to create wobbly structures
world = b2d.world(gravity=(0, -10))

# Create a ground body
edge = world.create_static_body(
    position=(0, 0), fixtures=b2d.fixture_def(shape=b2d.edge_shape([(-10, 0), (10, 0)]))
)

# create 3 bodies
a = world.create_dynamic_body(
    position=(-3, 4),
    fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=1), density=1),
)
b = world.create_dynamic_body(
    position=(3, 4),
    fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=1), density=1),
)
c = world.create_dynamic_body(
    position=(0, 8),
    fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=1), density=1),
)

# connect bodies with distance joints
distance_joint_def = dict(length=5, stiffness=100)
world.create_distance_joint(a, b, **distance_joint_def)
world.create_distance_joint(a, c, **distance_joint_def)
world.create_distance_joint(b, c, **distance_joint_def)

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10))
ani
plt.show()
