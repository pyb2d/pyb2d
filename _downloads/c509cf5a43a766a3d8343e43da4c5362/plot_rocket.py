"""
Rocket
===========================

Fly a rocket from one plant to another.
Use 'a','w','d' to fire the rockets engines,
but avoid the black hole!
"""

from b2d.testbed import TestbedBase
import random
import numpy
import b2d
import math


class Rocket(TestbedBase):

    name = "Rocket"

    def __init__(self, settings=None):
        super(Rocket, self).__init__(gravity=(0, 0), settings=settings)

        # gravitational constant
        self.gravitational_constant = 6.0

        self.planets = {}

        # home planet
        home_planet = self.world.create_kinematic_body(
            position=(10, 0),
            fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=20)),
            user_data="home_planet",
        )

        # target planet
        target_planet = self.world.create_kinematic_body(
            position=(100, 100),
            fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=10)),
            user_data="target_planet",
        )

        # black hole
        black_hole = self.world.create_kinematic_body(
            position=(0, 400),
            fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=1)),
            user_data="black_hole",
        )

        self.planets = {
            home_planet: dict(radius=20, density=1, color=(0, 0.2, 1)),
            target_planet: dict(radius=10, density=1, color=(0.7, 0.7, 0.7)),
            black_hole: dict(radius=1, density=10000, color=(0.1, 0.1, 0.1)),
        }

        # a tiny rocket
        self.rocket = self.world.create_dynamic_body(
            position=(10, 10),
            fixtures=[
                b2d.fixture_def(shape=b2d.polygon_shape(box=[1, 1]), density=1),
                b2d.fixture_def(
                    shape=b2d.polygon_shape(vertices=[(-1, 1), (0, 4), (1, 1)]),
                    density=1,
                ),
            ],
            angular_damping=0.5,
            linear_damping=0.2,
            user_data="rocket",
        )
        # check if the rocket is gone
        self.touched_black_hole = False

        # particle system
        pdef = b2d.particle_system_def(
            viscous_strength=0.9,
            spring_strength=0.0,
            damping_strength=100.5,
            pressure_strength=1.0,
            color_mixing_strength=0.05,
            density=0.1,
        )

        psystem = self.world.create_particle_system(pdef)
        psystem.radius = 0.1
        psystem.damping = 0.5

        self.emitters = []
        self.key_map = {"w": 0, "a": 1, "d": 2}

        angle_width = (math.pi * 2) / 16
        emitter_def = b2d.RandomizedRadialEmitterDef()
        emitter_def.emite_rate = 2000
        emitter_def.lifetime = 1.0
        emitter_def.enabled = False
        emitter_def.inner_radius = 1
        emitter_def.outer_radius = 1
        emitter_def.velocity_magnitude = 10.0
        emitter_def.start_angle = math.pi / 2 - angle_width / 2.0
        emitter_def.stop_angle = math.pi / 2 + angle_width / 2.0
        emitter_def.body = self.rocket

        delta = 0.2
        self.emitter_local_anchors = [
            (0, -delta),  # main
            (-delta, -0.5),  # left,
            (delta, -0.5),  # right
        ]
        self.emitter_local_rot = [math.pi, math.pi / 2, -math.pi / 2]  # main

        # main trust
        emitter_def.emite_rate = 2000
        world_anchor = self.rocket.get_world_point(self.emitter_local_anchors[0])
        emitter_def.transform = b2d.Transform(
            world_anchor, b2d.Rot(self.emitter_local_rot[0])
        )
        emitter = b2d.RandomizedRadialEmitter(psystem, emitter_def)
        self.emitters.append(emitter)

        # left
        emitter_def.emite_rate = 200
        world_anchor = self.rocket.get_world_point(self.emitter_local_anchors[1])
        emitter_def.transform = b2d.Transform(
            world_anchor, b2d.Rot(self.emitter_local_rot[1])
        )
        emitter = b2d.RandomizedRadialEmitter(psystem, emitter_def)
        self.emitters.append(emitter)

        # right
        emitter_def.emite_rate = 200
        world_anchor = self.rocket.get_world_point(self.emitter_local_anchors[1])
        emitter_def.transform = b2d.Transform(
            world_anchor, b2d.Rot(self.emitter_local_rot[1])
        )
        emitter = b2d.RandomizedRadialEmitter(psystem, emitter_def)
        self.emitters.append(emitter)

    def pre_step(self, dt):

        # check if the rocket has died
        if self.touched_black_hole:
            if self.rocket is not None:
                self.world.destroy_body(self.rocket)
                self.rocket = None
        else:
            rocket_center = self.rocket.world_center
            rocket_mass = self.rocket.mass
            # compute gravitational forces
            net_force = numpy.zeros([2])
            for planet, planet_def in self.planets.items():
                radius = planet_def["radius"]
                planet_center = planet.position
                planet_mass = planet_def["density"] * radius ** 2 * math.pi
                delta = rocket_center - planet_center
                distance = delta.normalize()
                f = (
                    -self.gravitational_constant
                    * rocket_mass
                    * planet_mass
                    / (distance * distance)
                )
                net_force += delta * f
            f = float(net_force[0]), float(net_force[1])
            self.rocket.apply_force_to_center(f)

            # run the rockets engines
            for emitter, local_anchor, local_rotation in zip(
                self.emitters, self.emitter_local_anchors, self.emitter_local_rot
            ):
                world_anchor = self.rocket.get_world_point(local_anchor)
                emitter.position = world_anchor
                emitter.angle = self.rocket.angle + local_rotation
                emitter.step(dt)

    def begin_contact(self, contact):
        body_a = contact.body_a
        body_b = contact.body_b
        if body_b.user_data == "rocket":
            body_a, body_b = body_b, body_a

        user_data_a = body_a.user_data
        user_data_b = body_b.user_data
        if body_a.user_data == "rocket":
            if user_data_b == "black_hole":
                self.touched_black_hole = True

    def on_keyboard_down(self, key):
        if key in self.key_map:
            self.emitters[self.key_map[key]].enabled = True
            return True
        return False

    def on_keyboard_up(self, key):
        if key in self.key_map:
            self.emitters[self.key_map[key]].enabled = False
            return False
        return False

    def pre_debug_draw(self):
        pass

    def post_debug_draw(self):
        for planet, planet_def in self.planets.items():
            pos = planet.position

            self.debug_draw.draw_solid_circle(
                pos, planet_def["radius"] + 0.1, axis=None, color=planet_def["color"]
            )
            if planet.user_data == "black_hole":
                self.debug_draw.draw_circle(
                    pos, planet_def["radius"] * 5, color=(1, 1, 1), line_width=0.1
                )


if __name__ == "__main__":

    ani = b2d.testbed.run(Rocket)
