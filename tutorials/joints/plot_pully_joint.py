"""
Pully Joint
===========================

Create a pully joint
Uses:
    * :class:`b2d.PullyJointDef`
    * :class:`b2d.PullyJoint`
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
# pully joint
world = b2d.world(gravity=(0, -10))


a = world.create_dynamic_body(
    position=(-5, 0),
    fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[2, 0.8]), density=1),
    linear_damping=0.0,
    angular_damping=0.0,
)
b = world.create_dynamic_body(
    position=(5, 0),
    fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[2, 0.5]), density=1),
    linear_damping=0.0,
    angular_damping=0.0,
)
world.create_pully_joint(
    a,
    b,
    length_a=10,
    length_b=10,
    ground_anchor_a=(-5, 10),
    ground_anchor_b=(5, 10),
    local_anchor_a=(0, 0),
    local_anchor_b=(0, 0),
)

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(20, 20))
ani
plt.show()
