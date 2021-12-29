from ._b2d import Vec2
from .testbed.backend.gif_gui.opencv_debug_draw import OpenCvBatchDebugDraw

import matplotlib.pyplot as plt
import numpy as np


def render_world(world, ppm=20, flags=None, world_margin=None):
    if world_margin is None:
        world_margin = Vec2(0, 0)
    world_margin = Vec2(world_margin[0], world_margin[1])

    lower_left, top_right = world.get_world_aabb()
    lower_left -= world_margin
    top_right += world_margin
    world_size = top_right - lower_left

    image_size = world_size * ppm
    shape = [int(image_size[0] + 0.5), int(image_size[1] + 0.5)]

    image = np.zeros(shape + [3], dtype="uint8")

    debug_draw = OpenCvBatchDebugDraw(image=image, flags=flags)
    debug_draw.flip_y = True
    debug_draw.scale = ppm
    debug_draw.screen_size = shape
    t = (-ppm * lower_left[0], -ppm * lower_left[1])
    debug_draw.translate = t

    # draw the world with a temporary debug draw
    # (will restore the old debug draw after the call)
    world.draw_debug_data_with_temporary(debug_draw)

    return image


def plot_world(*args, **kwargs):
    img = render_world(*args, **kwargs)
    img = np.swapaxes(img, 0, 1)
    axis = plt.imshow(img)

    # labels = axis.get_xticklabels()            # Get locations and labels
    # print(labels)
    # xticks(ticks, [labels], **kwargs)  # Set locations and labels
