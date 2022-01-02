"""
Weld Joint
===========================

Create weld joints
"""


# %%
# Imports
# ------------------------
#
# pyb2d is imported as `b2d`
import b2d
import numpy as np
import math

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


bodies = []

# create  a static body as anchor
b = world.create_static_body(
    position=(0, 4), fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[0.3, 0.5]))
)
bodies.append(b)

for i in range(10):
    b = world.create_dynamic_body(
        position=(i + 1.0, 4),
        fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[0.3, 0.5]), density=0.1),
        linear_damping=2.5,
        angular_damping=2.5,
    )
    bodies.append(b)

for i in range(len(bodies) - 1):
    a = bodies[i]
    b = bodies[i + 1]
    world.create_weld_joint(
        a,
        b,
        local_anchor_a=(0.5, 0.5),
        local_anchor_b=(-0.5, 0.5),
        damping=0.1,
        reference_angle=0,
        stiffness=20,
    )
    world.create_weld_joint(
        a,
        b,
        local_anchor_a=(0.5, -0.5),
        local_anchor_b=(-0.5, -0.5),
        damping=0.1,
        reference_angle=0,
        stiffness=20,
    )


fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10))
ani
plt.show()
