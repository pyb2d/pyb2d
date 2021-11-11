#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a simple example of building and running a simulation using Box2D. Here
we create a large ground box and a small dynamic box.

** NOTE **
There is no graphical output for this simple example, only text.
"""

from pybox2d import (polygon_shape, b2World)

world = b2World()  # default gravity is (0,-10) and doSleep is True
groundBody = world.create_static_body(position=(0, -10),
                                    shapes=polygon_shape(box=(50, 10)),
                                    )

# Create a dynamic body at (0, 4)
body = world.create_dynamic_body(position=(0, 4))

# And add a box fixture onto it (with a nonzero density, so it will move)
box = body.create_polygon_fixture(box=(1, 1), density=1, friction=0.3)

# Prepare for simulation. Typically we use a time step of 1/60 of a second
# (60Hz) and 6 velocity/2 position iterations. This provides a high quality
# simulation in most game scenarios.
timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2

# This is our little game loop.
for i in range(60):
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    world.Step(timeStep, vel_iters, pos_iters)

    # Clear applied body forces. We didn't apply any forces, but you should
    # know about this function.
    world.ClearForces()

    # Now print the position and angle of the body.
    print(body.position, body.angle)


# You can also work closer to the C++ Box2D library, not using the niceties
# supplied by pybox2d. Creating a world and a few bodies becomes much more
# verbose:
'''
    from pybox2d import (b2BodyDef, fixture_def)
    # Construct a world object, which will hold and simulate the rigid bodies.
    world = b2World(gravity=(0, -10), doSleep=True)

    # Define the ground body.
    groundBodyDef = b2BodyDef()
    groundBodyDef.position = (0, -10)

    # Make a body fitting this definition in the world.
    groundBody = world.create_body(groundBodyDef)

    # Create a big static box to represent the ground
    groundBox = polygon_shape(box=(50, 10))

    # And create a fixture definition to hold the shape
    groundBoxFixture = fixture_def(shape=groundBox)

    # Add the ground shape to the ground body.
    groundBody.CreateFixture(groundBoxFixture)
'''
