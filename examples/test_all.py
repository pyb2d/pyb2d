from plot_rocket import Rocket
from plot_color_mixing import ColorMixing
from plot_function_shape import FunctionShape
from plot_gauss_machine import GaussMachine
from plot_newtons_cradle import NewtonsCradle
from plot_blender import Blender
from plot_raycast import Raycast
from plot_angry_shapes import AngryShapes
from plot_billiard import Billiard
from plot_elliptic_billiard_table import EllipticBillardTable
from plot_goo import Goo

import b2d
from b2d.testbed.backend.no_gui import NoGui


import pytest


examples = [
    FunctionShape,
    NewtonsCradle,
    Blender,
    Raycast,
    Billiard,
    EllipticBillardTable,
]

lf_examples = [Rocket, ColorMixing, GaussMachine, AngryShapes, Goo]
if b2d.BuildConfiguration.LIQUID_FUN:
    examples.extend(lf_examples)


@pytest.mark.parametrize("example_cls", examples)
def test_eval(example_cls):
    print(f"\nSimulate `{example_cls.name}:`")
    example_cls.run(NoGui, gui_settings=NoGui.Settings())
