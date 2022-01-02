"""
Goo
===========================

This example shows how to implement a the basics of a WorldOfGoo clone
"""

from b2d.testbed import TestbedBase
from dataclasses import dataclass
import math
import random
import numpy
import b2d
from functools import partial
import networkx


def best_pairwise_distance(data, f, distance):
    n = len(data)
    best = (None, None, float("inf"))
    for i in range(n - 1):
        da = f(data[i])
        for j in range(i + 1, n):
            db = f(data[j])

            d = distance(da, db)
            if d < best[2]:
                best = (i, j, d)
    return best


def rand_color():
    return tuple([random.random() for i in range(3)])


class Level(object):
    def __init__(self, testbed):
        self.testbed = testbed
        self.world = testbed.world

        self.gap_size = 15
        self.kill_sensors_height = 0.5
        self.usable_size = 20
        self.h = 10
        self.end_zone_height = 3

        self.outline_verts = [
            (0, self.h),
            (0, 2 * self.h),
            (0, self.h),
            (self.usable_size, self.h),
            (self.usable_size, 0),
            (self.usable_size + self.gap_size, 0),
            (self.usable_size + self.gap_size, self.h),
            (2 * self.usable_size + self.gap_size, self.h),
            (2 * self.usable_size + self.gap_size, 2 * self.h),
        ]

        # outline of the level
        shape = b2d.chain_shape(vertices=numpy.flip(self.outline_verts, axis=0))
        self.outline = self.world.create_static_body(position=(0, 0), shape=shape)

        # kill sensors
        self.kill_sensor_pos = (
            self.usable_size + self.gap_size / 2,
            self.kill_sensors_height / 2,
        )

        shape = b2d.polygon_shape(box=(self.gap_size / 2, self.kill_sensors_height / 2))
        self._kill_sensor = self.world.create_static_body(
            position=self.kill_sensor_pos,
            fixtures=b2d.fixture_def(shape=shape, is_sensor=True),
        )
        self._kill_sensor.user_data = "destroyer"

        # end sensor
        shape = b2d.polygon_shape(box=(self.usable_size / 2, self.end_zone_height / 2))
        self._end_sensor = self.world.create_static_body(
            position=(
                1.5 * self.usable_size + self.gap_size,
                self.h + self.end_zone_height / 2,
            ),
            fixtures=b2d.fixture_def(shape=shape, is_sensor=True),
        )
        self._end_sensor.user_data = "goal"

        goo_radius = 1
        a = self.testbed.insert_goo(
            pos=(self.usable_size / 3, self.h + goo_radius), static=True
        )
        b = self.testbed.insert_goo(
            pos=(self.usable_size * 2 / 3, self.h + goo_radius), static=True
        )
        c = self.testbed.insert_goo(
            pos=(self.usable_size * 1 / 2, self.h + goo_radius + 4), static=False
        )

        self.testbed.connect_goos(a, b)
        self.testbed.connect_goos(a, c)
        self.testbed.connect_goos(b, c)

    def draw(self, debug_draw):

        # draw outline
        for i in range(len(self.outline_verts) - 1):
            debug_draw.draw_segment(
                self.outline_verts[i],
                self.outline_verts[i + 1],
                color=(1, 1, 0),
                line_width=0.3,
            )

        left = list(self.kill_sensor_pos)
        left[0] -= self.gap_size / 2
        left[1] += self.kill_sensors_height / 2

        right = list(self.kill_sensor_pos)
        right[0] += self.gap_size / 2
        right[1] += self.kill_sensors_height / 2
        debug_draw.draw_segment(left, right, (1, 0, 0), line_width=0.4)


class FindGoos(b2d.QueryCallback):
    def __init__(self):
        super(FindGoos, self).__init__()
        self.goos = []

    def report_fixture(self, fixture):
        body = fixture.body
        if body.user_data == "goo":
            self.goos.append(body)
        return True


class Goo(TestbedBase):

    name = "Goo"

    def __init__(self, settings=None):
        super(Goo, self).__init__(settings=settings)

        self.goo_graph = networkx.Graph()
        self.level = Level(testbed=self)

        # mouse related
        self.last_mouse_pos = None
        self.is_mouse_down = False

        # callback to draw tentative placement
        self.draw_callback = None

        # goos marked for destruction
        self.goo_to_destroy = []

        # joints marked for destruction
        self.joints_to_destroy = []
        self.gamma = 0.003
        self.break_threshold = 0.5

        # time point when goo can be inserted
        self.insert_time_point = 0
        self.insert_delay = 1.0

        # handle finishing of level
        self.with_goal_contact = dict()

        # amount of seconds one has to be in the finishing zone
        self.win_delay = 3.0

        # particle system will be defined an used on win!
        # this is then used for some kind of fireworks
        self.psystem = None
        self.emitter = None
        self.emitter_stop_time = None
        self.emitter_start_time = None

    # trigger some fireworks on win
    def on_win(self, win_body):

        if self.psystem is None:
            # particle system
            pdef = b2d.particle_system_def(
                viscous_strength=0.9,
                spring_strength=0.0,
                damping_strength=100.5,
                pressure_strength=1.0,
                color_mixing_strength=0.05,
                density=0.1,
            )

            self.psystem = self.world.create_particle_system(pdef)
            self.psystem.radius = 0.1
            self.psystem.damping = 0.5

            emitter_def = b2d.RandomizedRadialEmitterDef()
            emitter_def.emite_rate = 2000
            emitter_def.lifetime = 0.9
            emitter_def.enabled = True
            emitter_def.inner_radius = 0.0
            emitter_def.outer_radius = 0.1
            emitter_def.velocity_magnitude = 1000.0
            emitter_def.start_angle = 0
            emitter_def.stop_angle = 2 * math.pi
            emitter_def.transform = b2d.Transform(
                win_body.position + b2d.vec2(0, 20), b2d.Rot(0)
            )
            self.emitter = b2d.RandomizedRadialEmitter(self.psystem, emitter_def)
            self.emitter_stop_time = self.elapsed_time + 0.2

    def draw_goo(self, pos, angle, body=None):
        self.debug_draw.draw_solid_circle(pos, 1, axis=None, color=(1, 0, 1))
        self.debug_draw.draw_circle(pos, 1.1, (1, 1, 1), line_width=0.1)

        if body is not None:
            centers = [
                body.get_world_point((-0.3, 0.2)),
                body.get_world_point((0.3, 0.2)),
            ]
            for center in centers:
                self.debug_draw.draw_solid_circle(
                    center, 0.4, axis=None, color=(1, 1, 1)
                )
                self.debug_draw.draw_solid_circle(
                    center, 0.2, axis=None, color=(0, 0, 0)
                )

    def draw_edge(self, pos_a, pos_b, stress):
        no_stress = numpy.array([1, 1, 1])
        has_stress = numpy.array([1, 0, 0])
        color = (1.0 - stress) * no_stress + stress * has_stress
        color = tuple([float(c) for c in color])
        self.debug_draw.draw_segment(pos_a, pos_b, color=color, line_width=0.4)

    def insert_goo(self, pos, static=False):
        if static:
            f = self.world.create_static_body
        else:
            f = self.world.create_dynamic_body

        goo = f(
            position=pos,
            fixtures=b2d.fixture_def(shape=b2d.circle_shape(radius=1), density=1),
            user_data="goo",
        )
        self.goo_graph.add_node(goo)
        return goo

    def connect_goos(self, goo_a, goo_b):
        length = (goo_a.position - goo_b.position).length
        joint = self.world.create_distance_joint(
            goo_a,
            goo_b,
            stiffness=500,
            damping=0.1,
            length=length,
            user_data=dict(length=length, stress=0),
        )
        self.goo_graph.add_edge(goo_a, goo_b, joint=joint)

    def query_placement(self, pos):

        radius = 8

        # find all goos in around pos
        pos = b2d.vec2(pos)
        box = b2d.aabb(
            lower_bound=pos - b2d.vec2(radius, radius),
            upper_bound=pos + b2d.vec2(radius, radius),
        )
        query = FindGoos()
        self.world.query_aabb(query, box)
        goos = query.goos
        n_goos = len(goos)

        if n_goos >= 2:

            # try to insert to goo as edge between
            # 2 existing goos
            def distance(a, b, p):
                if self.goo_graph.has_edge(a[0], b[0]):
                    return float("inf")
                return numpy.linalg.norm((a[1] + b[1]) / 2 - p)

            i, j, best_dist = best_pairwise_distance(
                goos,
                f=lambda goo: (goo, numpy.array(goo.position)),
                distance=partial(distance, p=pos),
            )

            if best_dist < 0.8:

                def draw_callback():
                    self.draw_edge(goos[i].position, goos[j].position, stress=0)

                def insert_callack():
                    self.connect_goos(goos[i], goos[j])

                return True, draw_callback, insert_callack

            # try to insert the goo as brand new
            # goo and connect it with 2 existing goos
            f = lambda goo: (goo, (goo.position - b2d.vec2(pos)).length)

            def distance(a, b):
                if not self.goo_graph.has_edge(a[0], b[0]):
                    return float("inf")
                return a[1] + b[1]

            i, j, best_dist = best_pairwise_distance(goos, f=f, distance=distance)
            if best_dist < float("inf"):

                def draw_callback():

                    self.draw_edge(pos, goos[i].position, stress=0)
                    self.draw_edge(pos, goos[j].position, stress=0)
                    self.draw_goo(pos, angle=None)

                def insert_callack():
                    goo = self.insert_goo(pos=pos)
                    self.connect_goos(goo, goos[i])
                    self.connect_goos(goo, goos[j])

                return True, draw_callback, insert_callack

        return False, None, None

    def on_mouse_down(self, pos):
        self.last_mouse_pos = pos
        self.is_mouse_down = True
        can_be_placed, draw_callback, insert_callback = self.query_placement(pos)
        if can_be_placed:
            if self.elapsed_time < self.insert_time_point:
                return True
            self.draw_callback = draw_callback
            return True
        return False

    def on_mouse_move(self, pos):
        self.last_mouse_pos = pos
        if self.is_mouse_down:
            can_be_placed, draw_callback, insert_callback = self.query_placement(pos)
            if can_be_placed:
                if self.elapsed_time < self.insert_time_point:
                    return True
                self.draw_callback = draw_callback
                return True
            else:
                self.draw_callback = None
        return False

    def on_mouse_up(self, pos):
        self.last_mouse_pos = pos
        self.is_mouse_down = False
        self.draw_callback = None
        can_be_placed, draw_callback, insert_callback = self.query_placement(pos)
        if can_be_placed:
            if self.elapsed_time < self.insert_time_point:
                return True
            # self.draw_callback = draw_callback
            insert_callback()
            self.insert_time_point = self.elapsed_time + self.insert_delay
            return True
        return False

    def begin_contact(self, contact):
        body_a = contact.body_a
        body_b = contact.body_b
        if body_b.user_data == "goo":
            body_a, body_b = body_b, body_a

        user_data_a = body_a.user_data
        user_data_b = body_b.user_data
        if body_a.user_data == "goo":
            if user_data_b == "destroyer":
                self.goo_to_destroy.append(body_a)
            elif user_data_b == "goal":
                self.with_goal_contact[body_a] = self.elapsed_time + self.win_delay

    def end_contact(self, contact):
        body_a = contact.body_a
        body_b = contact.body_b
        if body_b.user_data == "goo":
            body_a, body_b = body_b, body_a

        user_data_a = body_a.user_data
        user_data_b = body_b.user_data
        if body_a.user_data == "goo":
            if user_data_b == "goal":
                if body_a in self.with_goal_contact:
                    del self.with_goal_contact[body_a]

    def pre_step(self, dt):

        # query if goo can be inserted
        if (
            self.is_mouse_down
            and self.last_mouse_pos is not None
            and self.draw_callback is None
        ):
            can_be_placed, draw_callback, insert_callback = self.query_placement(
                self.last_mouse_pos
            )
            if can_be_placed and self.elapsed_time >= self.insert_time_point:
                self.draw_callback = draw_callback

        # compute joint stress
        for goo_a, goo_b, joint in self.goo_graph.edges(data="joint"):
            jd = joint.user_data

            # distance based stress
            insert_length = jd["length"]
            length = (goo_a.position - goo_b.position).length

            d = length - insert_length
            if d > 0:

                # reaction force based stress
                rf = joint.get_reaction_force(30).length

                normalized_rf = 1.0 - math.exp(-rf * self.gamma)

                jd["stress"] = normalized_rf / self.break_threshold
                if normalized_rf > self.break_threshold:
                    self.joints_to_destroy.append((goo_a, goo_b, joint))

            else:
                jd["stress"] = 0

        for goo_a, goo_b, joint in self.joints_to_destroy:
            self.goo_graph.remove_edge(u=goo_a, v=goo_b)
            self.world.destroy_joint(joint)
        self.joints_to_destroy = []

        # destroy goos
        for goo in self.goo_to_destroy:
            self.goo_graph.remove_node(goo)
            self.world.destroy_body(goo)

        # destroy all with wrong degree
        while True:
            destroyed_any = False
            to_remove = []
            for goo in self.goo_graph.nodes:
                if self.goo_graph.degree(goo) < 2:
                    destroyed_any = True
                    to_remove.append(goo)
            if not destroyed_any:
                break
            for goo in to_remove:
                self.goo_graph.remove_node(goo)
                self.world.destroy_body(goo)
        self.goo_to_destroy = []

        # check if we are done
        for goo, finish_time in self.with_goal_contact.items():
            if finish_time <= self.elapsed_time:
                self.on_win(goo)

        if self.emitter is not None:
            if self.emitter_stop_time is not None:
                if self.elapsed_time > self.emitter_stop_time:
                    self.emitter.enabled = False
                    self.emitter_start_time = self.elapsed_time + 0.4
                    self.emitter_stop_time = None
                    p = list(self.emitter.position)
                    p[0] += (random.random() - 0.5) * 10.0
                    p[1] += (random.random() - 0.5) * 2.0
                    self.emitter.position = p
            if self.emitter_start_time is not None:
                if self.elapsed_time > self.emitter_start_time:
                    self.emitter.enabled = True
                    self.emitter_start_time = None
                    self.emitter_stop_time = self.elapsed_time + 0.2
            self.emitter.step(dt)

    def post_debug_draw(self):

        self.level.draw(self.debug_draw)

        # draw mouse when mouse is down
        if (
            self.is_mouse_down
            and self.last_mouse_pos is not None
            and self.draw_callback is None
        ):
            d = (self.insert_time_point - self.elapsed_time) / self.insert_delay
            if d > 0:
                d = d * math.pi * 2
                x = math.sin(d)
                y = math.cos(d)
                p = self.last_mouse_pos[0] + x, self.last_mouse_pos[1] + y
                self.debug_draw.draw_segment(
                    p, self.last_mouse_pos, color=(1, 0, 0), line_width=0.2
                )
            self.debug_draw.draw_circle(
                self.last_mouse_pos, 1, (1, 0, 0), line_width=0.2
            )

        # draw the tentative placement
        if self.draw_callback is not None:
            self.draw_callback()

        for goo_a, goo_b, joint in self.goo_graph.edges(data="joint"):
            self.draw_edge(
                goo_a.position, goo_b.position, stress=joint.user_data["stress"]
            )

        for goo in self.goo_graph:
            self.draw_goo(goo.position, goo.angle, body=goo)


if __name__ == "__main__":
    ani = b2d.testbed.run(Goo)
    ani
