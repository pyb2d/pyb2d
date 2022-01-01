"""
Revolute Joint
===========================

Create revolute joints
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
# revolute joints
world = b2d.world(gravity=(0, -10))
bodies = []
b = world.create_static_body(
    position=(0, 15),
)
bodies.append(b)
for i in range(5):
    b = world.create_dynamic_body(
        position=(i * 4 + 2, 15),
        fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[2, 0.5]), density=1),
        linear_damping=0.0,
        angular_damping=0.0,
    )
    bodies.append(b)
world.create_revolute_joint(
    bodies[0], bodies[1], local_anchor_a=(0, 0), local_anchor_b=(-2, 0.0)
)
for i in range(1, len(bodies) - 1):
    a = bodies[i]
    b = bodies[i + 1]
    world.create_revolute_joint(a, b, local_anchor_a=(2, 0.0), local_anchor_b=(-2, 0.0))


fig, ax, ani = b2d.plot.animate_world(world, world_margin=(20, 20))
ani
plt.show()
