from color_mixing import ColorMixing
from function_shape import FunctionShape
from gauss_machine import GaussMachine
from newtons_cradle import NewtonsCradle

import b2d
from b2d.testbed.backend.no_gui import NoGui



examples = [
    FunctionShape,
    NewtonsCradle,
    Blender
]

lf_examples = [
    ColorMixing,
    GaussMachine,
]


if b2d.BuildConfiguration.LIQUID_FUN:
    examples.extend(lf_examples)





if __name__ == "__main__":

    for example_cls in examples:

        print(f"\nRender `{example_cls.name}:`")
        from b2d.testbed.backend.gif_gui import GifGui
        gui_settings = {
            "fps" : 30,
            "t" : 20,
            "filename" : f"{example_cls.name}.gif"
        }
        testbed, gui = example_cls.run(GifGui, gui_settings=gui_settings)

