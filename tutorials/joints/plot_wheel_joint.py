"""
Wheel Joint
===========================

Create a car with two wheel and wheel joints

Uses:
    * :class:`b2d.WheelJointDef`
    * :class:`b2d.WheelJoint`
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
# The world and ground body
world = b2d.world(gravity=(0, -10))
edge = world.create_static_body(
    position=(0, 0), fixtures=b2d.fixture_def(shape=b2d.edge_shape([(-20, 0), (5, 0)]))
)

# random slope
x = np.linspace(5, 50, 10)
y = np.random.rand(10) * 4 - 2
y[0] = 0
xy = np.stack([x, y]).T
xy = np.flip(xy, axis=0)
edge = world.create_static_body(
    position=(0, 0),
    fixtures=b2d.fixture_def(shape=b2d.chain_shape(xy, prev_vertex=(10, 0))),
)

# %%
# create car
left_wheel = world.create_dynamic_body(
    position=(-3, 2),
    fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=2), density=1),
)
right_wheel = world.create_dynamic_body(
    position=(3, 2),
    fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=2), density=1),
)

chasis = world.create_dynamic_body(
    position=(0, 2),
    fixtures=b2d.fixture_def(shape=b2d.polygon_shape(box=[3, 0.5]), density=1),
)

wheel_joint_def = dict(
    stiffness=10,
    enable_motor=True,
    motor_speed=-100,
    max_motor_torque=100,
    collide_connected=False,
    enable_limit=True,
    lower_translation=-0.4,
    upper_translation=0.4,
    local_axis_a=(0, 1),
)
world.create_wheel_joint(chasis, left_wheel, local_anchor_a=(-3, 0), **wheel_joint_def)
world.create_wheel_joint(chasis, right_wheel, local_anchor_a=(3, 0), **wheel_joint_def)

fig, ax, ani = b2d.plot.animate_world(world, world_margin=(10, 10), t=5)
ani
plt.show()
