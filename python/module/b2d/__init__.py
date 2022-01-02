from abc import ABC
import numbers


from ._b2d import *
from .tools import *
from .extend_math import *
from .extend_draw import *
from .extend_world import *
from .extend_body import *
from .extend_fixture import *
from .extend_shapes import *
from .extend_shapes import EdgeShape
from .extend_joints import *
from .extend_collision import *
from .extend_contact import *
from .extend_batch_api import *
from .query_callback import *

if BuildConfiguration.LIQUID_FUN:
    from .extend_particles import *
# from . destruction_listener import DestructionListener

__version__ = _b2d.__version__


class RayCastCallback(RayCastCallbackCaller):
    def __init__(self):
        super(RayCastCallback, self).__init__(self)

    def report_fixture(self, fixture, point, normal, fraction):
        raise NotImplementedError

    # def report_particle(self, particleSystem, index):
    #    return False
    # def should_query_particle_system(self, particleSystem):
    #    return False


class ContactListener(ContactListenerCaller):
    def __init__(self):
        super(ContactListener, self).__init__(self)

    # def begin_contact(self, contact):
    #     pass

    # def end_contact(self, contact):
    #     pass

    # def begin_contact_particle_body(self, particleSystem, particleBodyContact):
    #     pass

    # def begin_contact_particle(self, particleSystem, indexA, indexB):
    #     pass

    # def end_contact_particle(self, particleSystem, indexA, indexB):
    #     pass

    # def pre_solve(self, contact, oldManifold):
    #     pass

    # def post_solve(self, contact, impulse):
    #     pass


def batch_debug_draw_caller_cls(float_colors, float_coordinates, with_transform):

    color_type = ["uint8", "float"][float_colors]
    coordinate_type = ["int32", "float"][float_coordinates]

    cls_name = f"BatchDebugDrawCaller_{color_type}_{coordinate_type}_{with_transform}"

    return getattr(_b2d, cls_name)


def batch_debug_draw_cls(float_colors, float_coordinates, with_transform):

    base_cls = batch_debug_draw_caller_cls(
        float_colors, float_coordinates, with_transform
    )

    class BatchDebugDraw(base_cls):
        def __init__(self):
            super(BatchDebugDraw, self).__init__(self)

        def begin_draw(self):
            pass

        def end_draw(self):
            pass

        def draw_solid_polygons(self, points, connect, color):
            pass

        def draw_polygons(self, points, connect, color):
            pass

        def draw_segments(self, points, connect, color):
            pass

        def draw_solid_circles(self, centers, radii, axis, color):
            pass

        def draw_circles(self, centers, radii, color):
            pass

        def draw_particles(self, centers, radius, colors):
            pass

        def append_flags(self, flag_list_or_int):
            if isinstance(flag_list_or_int, numbers.Number):
                self._append_flags_int(flag_list_or_int)
            else:
                flag_list = flag_list_or_int
                if isinstance(flag_list, str):
                    flag_list = [flag_list]
                for flag in flag_list:
                    self._append_flags_int(draw_flags_dict[flag])

        def clear_flags(self, flag_list_or_int):
            if isinstance(flag_list_or_int, numbers.Number):
                self._clear_flags_int(flag_list_or_int)
            else:
                flag_list = flag_list_or_int
                if isinstance(flag_list, str):
                    flag_list = [flag_list]
                for flag in flag_list:
                    self._clear_flags_int(draw_flags_dict[flag])

    return BatchDebugDraw


class ContactFilter(ContactFilterCaller):
    def __init__(self):
        super(ContactFilter, self).__init__(self)

    def should_collide_fixture_fixture(self, fixtureA, fixtureB):
        pass

    def should_collide_fixture_particle(self, fixture, particleSystem, particleIndex):
        pass

    def should_collide_particle_particle(
        self, particleSystem, particleIndexA, particleIndexB
    ):
        pass


class DestructionListener(DestructionListenerCaller):
    def __init__(self):
        super(DestructionListener, self).__init__(self)

    def say_goodbye_joint(self, joint):
        pass

    def say_goodbye_fixture(self, fixture):
        pass

    def say_goodbye_particle_group(self, particleGroup):
        pass

    def say_goodbye_particle_system(self, particleSystem, index):
        pass
