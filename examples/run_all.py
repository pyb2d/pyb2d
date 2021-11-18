from color_mixing import ColorMixing
from function_shape import FunctionShape
from gauss_machine import GaussMachine

from b2d.testbed.backend.no_gui import NoGui


if __name__ == "__main__":
    gui_settings = {
    }

    examples = [
        ColorMixing,
        FunctionShape,
        GaussMachine,
    ]
    for example_cls in examples:
        print(f"Simulate `{example_cls.name}:`")
        example_cls.run(NoGui, gui_settings=gui_settings)