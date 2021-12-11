
from dataclasses import dataclass,field

def list_field(default_value):
    return field(default_factory=lambda:list(default_value))


class GuiBase(object):

    @dataclass
    class Settings:

        # the gui is responsible for "driving the world"
        # at a certain fps
        fps: float = 40



        resolution: list = list_field([1000,1000])
        scale: float = 20
        translate: list = list_field([200,200])


        draw_shape: bool = True
        draw_joint: bool = True
        draw_aabb: bool = False
        draw_pair: bool = False
        draw_center_of_mass: bool = False
        draw_particle: bool = False