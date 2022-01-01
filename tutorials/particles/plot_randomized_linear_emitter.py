"""
Emitter
===========================

Create a RandomizedLinearEmitter
"""

# %%
# Imports
# ------------------------
import b2d
import numpy as np
import b2d.plot
import matplotlib.pyplot as plt

# %%
# create world and a particle system
world = b2d.world(gravity=(0, -10))
pdef = b2d.particle_system_def(radius=0.1)
psystem = world.create_particle_system(pdef)

# %%
# create a  linear emitter
emitter_pos = (0, 0)
emitter_def = b2d.RandomizedLinearEmitterDef()
emitter_def.emite_rate = 400
emitter_def.lifetime = 5.1
emitter_def.size = (2, 1)
# emitter_def.transform = b2d.Transform(emitter_pos, b2d.Rot(0))
emitter_def.velocity = (6, 20)
emitter = b2d.RandomizedLinearEmitter(psystem, emitter_def)

# %%
# look at the world
fig, ax, ani = b2d.plot.animate_world(
    world, ppm=20, bounding_box=((-10, -20), (20, 15)), pre_step=emitter.step, t=5
)
ani
plt.show()
