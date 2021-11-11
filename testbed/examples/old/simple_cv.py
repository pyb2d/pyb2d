#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A small self contained example showing how to use OpencvDrawFuncs
to integrate pybox2d into an opencv mainloop

In short:
One static body:
    + One fixture: big polygon to represent the ground
Two dynamic bodies:
    + One fixture: a polygon
    + One fixture: a circle
And some drawing code that extends the shape classes.

John Stowers
"""
import cv2

import Box2D
from Box2D.b2 import (polygonShape, world)
from opencv_draw import OpencvDrawFuncs

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.create_static_body(
    position=(0, 0),
    shapes=polygonShape(box=(50, 1)),
)

# Create a couple dynamic bodies
bodyc = world.create_dynamic_body(position=(20, 45))
circle = bodyc.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

body_b = world.create_dynamic_body(position=(30, 45), angle=15)
box = body_b.create_polygon_fixture(box=(2, 1), density=1, friction=0.3)

world.CreateWeldJoint(body_a=bodyc, body_b=body_b, anchor=body_b.worldCenter)

drawer = OpencvDrawFuncs(w=640, h=480, ppm=20)
drawer.install()

while True:
    key = 0xFF & cv2.waitKey(int(TIME_STEP * 1000))  # milliseconds
    if key == 27:
        break
    drawer.clear_screen()

    drawer.draw_world(world)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    cv2.imshow("world", drawer.screen)
