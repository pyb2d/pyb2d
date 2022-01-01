from ._b2d import Vec2
from .extend_math import vec2
from .testbed.backend.gif_gui.opencv_debug_draw import OpenCvBatchDebugDraw

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def render_world(world, ppm=20, flags=None, world_margin=None, bounding_box=None):
    if world_margin is None:
        world_margin = Vec2(0, 0)
    world_margin = Vec2(world_margin[0], world_margin[1])

    if bounding_box is None:
        lower_left, top_right = world.get_world_aabb()
    else:
        lower_left, top_right = bounding_box

    lower_left = vec2(lower_left)
    top_right = vec2(top_right)
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
    def callback():
        world.draw_debug_data()

    world.with_temporary_debug_draw(debug_draw, callback=callback)

    return image


def plot_world(*args, **kwargs):
    img = render_world(*args, **kwargs)
    img = np.swapaxes(img, 0, 1)
    return plt.imshow(img)

    # labels = axis.get_xticklabels()            # Get locations and labels
    # print(labels)
    # xticks(ticks, [labels], **kwargs)  # Set locations and labels


def animate_world(
    world,
    ppm=20,
    flags=None,
    world_margin=None,
    fps=24,
    t=3,
    bounding_box=None,
    pre_step=None,
    post_step=None,
):
    if world_margin is None:
        world_margin = Vec2(0, 0)
    world_margin = Vec2(world_margin[0], world_margin[1])

    if bounding_box is None:
        lower_left, top_right = world.get_world_aabb()
    else:
        lower_left, top_right = bounding_box

    lower_left = vec2(lower_left)
    top_right = vec2(top_right)

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
    translate = (-ppm * lower_left[0], -ppm * lower_left[1])
    debug_draw.translate = translate

    dt = 1.0 / fps
    n_steps = int(t / dt + 0.5)

    image_list = []

    def callback():
        world.draw_debug_data()
        image_list.append(np.swapaxes(image.copy(), 0, 1))
        image[...] = 0
        for i in range(n_steps):
            if pre_step is not None:
                pre_step(dt)
            world.step(dt / 2, 5, 5)
            world.step(dt / 2, 5, 5)
            if post_step is not None:
                post_step(dt)
            world.draw_debug_data()
            image_list.append(np.swapaxes(image.copy(), 0, 1))
            image[...] = 0

    world.with_temporary_debug_draw(debug_draw, callback=callback)

    fig, ax = plt.subplots()
    imshow = plt.imshow(image_list[0])

    def _update_plt(num):
        imshow.set_data(image_list[num])
        return (imshow,)

    ani = animation.FuncAnimation(
        fig,
        _update_plt,
        frames=len(image_list),
        interval=dt * 1000.0,
        blit=True,
        save_count=len(image_list),
        repeat_delay=500,
        cache_frame_data=False,
    )
    # plt.show()
    return fig, ax, ani
