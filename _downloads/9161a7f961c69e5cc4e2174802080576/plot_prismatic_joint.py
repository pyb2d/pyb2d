"""
Prismatic Joint
===========================

Create a prismatic joint
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
# prismatic joint
world = b2d.world(gravity=(0, -10))

anchor_body = world.create_static_body(position=(0, 0))


b = world.create_dynamic_body(
    position=(10, 10),
    fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[2, 0.5]), density=1),
    linear_damping=0.0,
    angular_damping=0.0,
)
world.create_prismatic_joint(anchor_body, b, local_axis_a=(1, 1))


fig, ax, ani = b2d.plot.animate_world(world, world_margin=(20, 20))
ani
plt.show()
