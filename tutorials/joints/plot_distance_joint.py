"""
Distance Joint
===========================

Create distance joints
"""


# %%
# Imports
# ------------------------
#
# pyb2d is imported as `b2d`
import b2d
import numpy as np


# %%
# These imports are only needed for plotting.
# `b2d.plot` requires OpenCV to be installed!

import b2d.plot
import matplotlib.pyplot as plt


# %%
# The first step with Box2D is the creation
# of the world. The world is parametrized by a gravity
# vector.

# the world
world = b2d.world(gravity=(0, -10))

# %%
# Create a ground body
edge = world.create_static_body(
    position=(0, 0),
    fixtures=b2d.fixture_def(shape=b2d.edge_shape([(-10, 0), (10, 0)])),
)

# %%
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


# %%
# connect bodies with distance joints
distance_joint_def = dict(length=5, stiffness=100)
world.create_distance_joint(a, b, **distance_joint_def)
world.create_distance_joint(a, c, **distance_joint_def)
world.create_distance_joint(b, c, **distance_joint_def)

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10))
ani
plt.show()
