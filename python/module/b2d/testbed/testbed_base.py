import b2d
import numpy
import random
import time
from pydantic import BaseModel


class DebugDrawCallback(object):
    def __init__(self, pre_debug_draw, post_debug_draw):
        self._pre_debug_draw = pre_debug_draw
        self._post_debug_draw = post_debug_draw

    def pre_debug_draw(self):
        self._pre_debug_draw()

    def post_debug_draw(self):
        self._post_debug_draw()


class TestbedDestructionListener(b2d.DestructionListener):
    def __init__(self, testbed):
        b2d.DestructionListener.__init__(self)
        self.testbed = testbed

    def say_goodbye_joint(self, joint):
        self.testbed.internal_say_goodbye_joint(joint)

    def say_goodbye_fixture(self, fixture):
        self.testbed.say_goodbye_fixture(fixture)

    def say_goodbye_particle_group(self, particleGroup):
        self.testbed.say_goodbye_particle_group(particleGroup)

    def say_goodbye_particle_system(self, particleSystem, index):
        self.testbed.say_goodbye_particle_system(particleSystem, index)


class TestbedBase(b2d.ContactListener):
    class Settings(BaseModel):
        substeps: int = 1
        n_velocity_steps: int = 1
        n_position_iterations: int = 1

    @classmethod
    def run(cls, gui_cls, gui_settings=None, settings=None):
        if gui_settings is None:
            gui_settings = gui_cls.Settings()

        if settings is None:
            settings = cls.Settings()

        ui = gui_cls(testbed_cls=cls, testbed_settings=settings, settings=gui_settings)

        return ui.start_ui()

    def __init__(self, gravity=b2d.vec2(0, -9.81), settings=None):
        if settings is None:
            settings = self.Settings()
        self.settings = settings
        b2d.ContactListener.__init__(self)

        # Box2D-related
        self.world = None
        self.mouse_joint = None

        # self.framework_settings = FrameworkSettings
        self.step_count = 0
        self.is_paused = False
        self.__time_last_step = None
        self.current_fps = 0.0

        # the b2d world itself
        self.world = b2d.world(gravity)
        self.groundbody = self.world.create_body()

        # listeners
        self.destruction_listener = TestbedDestructionListener(testbed=self)
        self.world.set_contact_listener(self)
        self.world.set_destruction_listener(self.destruction_listener)
        self.iter = 0
        self.elapsed_time = 0.0

        # debug draw
        self.debug_draw = None

    def set_debug_draw(self, debug_draw):
        if self.debug_draw is not None:
            raise RuntimeError("debug draw has already been set")
        self.debug_draw = debug_draw
        self.world.set_debug_draw(self.debug_draw)

    def post_post_debug_draw(self):
        pass

    def pre_debug_draw(self):
        pass

    def post_debug_draw(self):
        pass

    def draw_debug_data(self):

        self.pre_debug_draw()
        self.world.draw_debug_data()
        self.post_debug_draw()

    def set_gui(self, gui):
        self._gui = gui

    def is_key_down(self, key):
        return self._gui.is_key_down(key)

    def step(self, dt):
        # pre stepping
        self.pre_step(dt)

        # stepping
        sub_dt = dt / self.settings.substeps
        for i in range(self.settings.substeps):
            self.world.step(
                sub_dt,
                self.settings.n_velocity_steps,
                self.settings.n_position_iterations,
            )

        # book-keeping
        self.elapsed_time += dt
        self.step_count += 1
        self.iter += 1

        # draw debug data
        self.draw_debug_data()

        # post stepping
        self.post_step(dt)

    def say_goodbye_world(self):
        pass

    def pre_step(self, dt):
        pass

    def post_step(self, dt):
        pass

    def get_particle_parameter_value(self):
        return 0

    def on_keyboard_down(self, keycode):
        return False

    def on_keyboard_up(self, keycode):
        return False

    def on_mouse_move(self, p):
        """
        Mouse moved to point p, in world coordinates.
        """
        if self.mouse_joint is not None:
            self.mouse_joint.target = p
            return True
        else:
            return False

    def on_mouse_down(self, p):
        """
        Indicates that there was a left click at point p (world coordinates)
        """

        if self.mouse_joint is not None:
            self.world.destroy_joint(self.mouse_joint)
            self.mouse_joint = None
            return False

        body = self.world.find_body(pos=p)
        if body is not None:

            kwargs = dict(
                body_a=self.groundbody,
                body_b=body,
                target=p,
                max_force=50000.0 * body.mass,
                stiffness=1000.0,
            )

            self.mouse_joint = self.world.create_mouse_joint(**kwargs)
            body.awake = True

        return body is not None

    def on_mouse_up(self, p):
        """
        Left mouse button up.
        """
        if self.mouse_joint is not None:
            self.world.destroy_joint(self.mouse_joint)
            self.mouse_joint = None
            return True
        else:
            return False

    def on_key_down(self, key):
        return False

    def on_key_up(self, key):
        return False

    # # ContactListener
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
    #    pass

    # DestructionListener
    def internal_say_goodbye_joint(self, joint):
        if joint == self.mouse_joint:
            self.mouse_joint = None
        else:
            self.say_goodbye_joint(joint)

    def say_goodbye_joint(self, joint):
        pass

    def say_goodbye_fixture(self, fixture):
        pass

    def say_goodbye_particle_group(self, particleGroup):
        pass

    def say_goodbye_particle_system(self, particleSystem, index):
        pass
