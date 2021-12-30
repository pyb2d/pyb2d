"""
AngryShapes
===========================

This example shows how to create games inspired by AngryBirds.
"""


from b2d.testbed import TestbedBase
import math
import numpy
import b2d


class AngryShapes(TestbedBase):

    name = "AngryShapes"

    class Settings(TestbedBase.Settings):
        substeps: int = 2

    def draw_segment(self, p1, p2, color, line_width=1):
        screen_p1 = self._point(self.world_to_screen(p1))
        screen_p2 = self._point(self.world_to_screen(p2))
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)

        cv.line(self._image, screen_p1, screen_p2, screen_color, screen_line_width)

    def draw_polygon(self, vertices, color, line_width=1):
        # todo add C++ function for this
        screen_vertices = numpy.array(
            [self._point(self.world_to_screen(v)) for v in vertices], dtype="int32"
        )
        screen_color = self._uint8_color(color)
        screen_line_width = self._line_width(line_width)

        cv.polylines(
            self._image, [screen_vertices], True, screen_color, screen_line_width, 8
        )

    def draw_solid_polygon(self, vertices, color):
        # todo add C++ function for this
        screen_vertices = numpy.array(
            [self._point(self.world_to_screen(v)) for v in vertices], dtype="int32"
        )
        screen_color = self._uint8_color(color)

        cv.fillPoly(self._image, [screen_vertices], screen_color, 8)

    def __init__(self, settings=None):
        super(AngryShapes, self).__init__(settings=settings)

        self.targets = []
        self.projectiles = []
        self.marked_for_destruction = []
        self.emitter = None

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
        self.psystem.radius = 1
        self.psystem.damping = 0.5

        self.build_outer_box()
        self.build_castle()
        self.build_launcher()
        self.arm_launcher()
        self.build_explosives()

    def build_outer_box(self):
        # the outer box

        shape = b2d.edge_shape([(100, 0), (600, 0)])
        box = self.world.create_static_body(
            position=(0, 0), fixtures=b2d.fixture_def(shape=shape, friction=1)
        )

    def build_target(self, pos):
        t = self.world.create_dynamic_body(
            position=pos,
            fixtures=[
                b2d.fixture_def(shape=b2d.circle_shape(radius=4), density=1.0),
                b2d.fixture_def(
                    shape=b2d.circle_shape(radius=2, pos=(3, 3)), density=1.0
                ),
                b2d.fixture_def(
                    shape=b2d.circle_shape(radius=2, pos=(-3, 3)), density=1.0
                ),
            ],
            linear_damping=0,
            angular_damping=0,
            user_data="target",
        )
        self.targets.append(t)

    def build_castle(self):
        def build_pyramid(offset, bar_shape, n):
            def build_brick(pos, size):
                hsize = [s / 2 for s in size]
                self.world.create_dynamic_body(
                    position=(
                        pos[0] + hsize[0] + offset[0],
                        pos[1] + hsize[1] + offset[1],
                    ),
                    fixtures=b2d.fixture_def(
                        shape=b2d.polygon_shape(box=hsize), density=8
                    ),
                    user_data="brick",
                )

            bar_length = bar_shape[0]
            bar_width = bar_shape[1]

            nxm = n
            for y in range(nxm):
                py = y * (bar_length + bar_width)
                nx = nxm - y
                for x in range(nx):
                    px = x * bar_length + y * (bar_length) / 2.0
                    if y + 1 < nxm - 1:
                        if x == 0:
                            px += bar_width / 2
                        if x + 1 == nx:
                            px -= bar_width / 2

                    build_brick((px, py), (bar_width, bar_length))
                    if x < nx - 1:
                        self.build_target(
                            pos=(
                                px + offset[0] + bar_length / 2,
                                py + offset[1] + bar_width,
                            )
                        )
                        build_brick(
                            (px + bar_width / 2, py + bar_length),
                            (bar_length, bar_width),
                        )

        build_pyramid(offset=(100, 0), bar_shape=[40, 4], n=4)
        build_pyramid(offset=(400, 0), bar_shape=[30, 3], n=4)

    def build_launcher(self):

        self.launcher_anchor_pos = (30, 0)
        self.launcher_anchor = self.world.create_static_body(
            position=self.launcher_anchor_pos
        )

    def arm_launcher(self):
        self.reload_time = None
        self.is_armed = True
        self.projectile_radius = 3
        projectile_pos = (self.launcher_anchor_pos[0], self.launcher_anchor_pos[1] / 2)

        self.projectile = self.world.create_dynamic_body(
            position=projectile_pos,
            fixtures=b2d.fixture_def(
                shape=b2d.circle_shape(radius=self.projectile_radius), density=100.0
            ),
            linear_damping=0,
            angular_damping=0,
            user_data="projectile",
        )
        self.projectiles.append(self.projectile)
        self.projectile_joint = self.world.create_distance_joint(
            self.launcher_anchor, self.projectile, length=1, stiffness=10000
        )
        self.mouse_joint = None

    def build_explosives(self):
        self.explosives = []

    def on_mouse_down(self, p):
        if self.is_armed:
            body = self.world.find_body(pos=p)
            if body is not None and body.user_data is not None:
                print("got body")
                if body.user_data == "projectile":
                    print("got projectile")
                    kwargs = dict(
                        body_a=self.groundbody,
                        body_b=body,
                        target=p,
                        max_force=50000.0 * body.mass,
                        stiffness=10000.0,
                    )

                    self.mouse_joint = self.world.create_mouse_joint(**kwargs)
                    body.awake = True
                    return True

        return False

    def on_mouse_move(self, p):
        if self.is_armed:
            if self.mouse_joint is not None:
                self.mouse_joint.target = p
                return True
        return False

    def on_mouse_up(self, p):
        if self.is_armed:
            if self.mouse_joint is not None:
                self.world.destroy_joint(self.mouse_joint)
                if self.projectile_joint is not None:
                    self.world.destroy_joint(self.projectile_joint)
                self.projectile_joint = None
                self.mouse_joint = None
                delta = self.launcher_anchor.position - b2d.vec2(p)
                scaled_delta = delta * 50000.0
                print(scaled_delta)

                self.projectile.apply_linear_impulse_to_center(scaled_delta, True)
                self.reload_time = self.elapsed_time + 1.0
                self.is_armed = False
        return False

    def begin_contact(self, contact):
        body_a = contact.body_a
        body_b = contact.body_b
        ud_a = body_a.user_data
        ud_b = body_b.user_data
        if ud_b == "projectile":
            body_a, body_b = body_b, body_a
            ud_a, ud_b = ud_b, ud_a
        if ud_a == "projectile":

            if ud_b == "target" or ud_b == "brick":
                self.marked_for_destruction.append(body_a)
                print("WUP")
                emitter_def = b2d.RandomizedRadialEmitterDef()
                emitter_def.emite_rate = 20000
                emitter_def.lifetime = 0.7
                emitter_def.enabled = True
                emitter_def.inner_radius = 0.0
                emitter_def.outer_radius = 1.0
                emitter_def.velocity_magnitude = 1000.0
                emitter_def.start_angle = 0
                emitter_def.stop_angle = math.pi
                emitter_def.transform = b2d.Transform(body_a.position, b2d.Rot(0))
                self.emitter = b2d.RandomizedRadialEmitter(self.psystem, emitter_def)
                self.emitter_die_time = self.elapsed_time + 0.02

    def pre_step(self, dt):

        if self.reload_time is not None:
            if self.elapsed_time >= self.reload_time:
                self.arm_launcher()

        # delete contact bodies
        for body in self.marked_for_destruction:
            if body in self.projectiles:
                self.projectiles.remove(body)
                self.world.destroy_body(body)
            if body == self.projectile:
                self.reload_time = self.elapsed_time + 1.0
            self.marked_for_destruction = []

        # delete bodies which have fallen down
        for body in self.world.bodies:
            if body.position.y < -100:
                if body.user_data == "projectile":
                    self.projectiles.remove(body)
                if body.user_data == "target":
                    self.targets.remove(body)
                self.world.destroy_body(body)

        # emmiter
        if self.emitter is not None:
            self.emitter.step(dt)
            if self.elapsed_time >= self.emitter_die_time:
                self.emitter = None

    def draw_target(self, target):
        center = target.position
        center_l = target.get_world_point((-3, 3))
        center_r = target.get_world_point((3, 3))
        eye_left = target.get_world_point((-1, 1))
        eye_right = target.get_world_point((1, 1))
        pink = [c / 255 for c in (248, 24, 148)]

        self.debug_draw.draw_solid_circle(
            center=center, radius=4, axis=None, color=pink
        )
        self.debug_draw.draw_solid_circle(
            center=center_l, radius=2, axis=None, color=pink
        )
        self.debug_draw.draw_solid_circle(
            center=center_r, radius=2, axis=None, color=pink
        )

        # schnautze
        nose_center = target.get_world_point((0, -1))
        nose_center_l = target.get_world_point((-0.3, -1))
        nose_center_r = target.get_world_point((0.3, -1))

        self.debug_draw.draw_circle(
            center=nose_center,
            radius=2,
            # axis=None,
            color=(1, 1, 1),
            line_width=0.2,
        )
        # eyes
        for nose_center in [nose_center_l, nose_center_r]:
            self.debug_draw.draw_solid_circle(
                center=nose_center, radius=0.6, axis=None, color=(1, 1, 1)
            )
        # eyes
        for eye_center in [eye_left, eye_right]:
            self.debug_draw.draw_solid_circle(
                center=eye_center, radius=1, axis=None, color=(1, 1, 1)
            )
            self.debug_draw.draw_solid_circle(
                center=eye_center, radius=0.7, axis=None, color=(0, 0, 0)
            )

    def draw_projectile(self, projectile):

        center = projectile.position
        # center_l = target.get_world_point((-3,3))
        # center_r = target.get_world_point(( 3,3))
        eye_left = projectile.get_world_point((-1, 1))
        eye_right = projectile.get_world_point((1, 1))

        self.debug_draw.draw_solid_circle(
            center=center,
            radius=self.projectile_radius * 1.1,
            axis=None,
            color=(1, 0, 0),
        )

        # eyes
        for eye_center in [eye_left, eye_right]:
            self.debug_draw.draw_solid_circle(
                center=eye_center, radius=1, axis=None, color=(1, 1, 1)
            )
            self.debug_draw.draw_solid_circle(
                center=eye_center, radius=0.7, axis=None, color=(0, 0, 0)
            )

    def post_debug_draw(self):
        for target in self.targets:
            self.draw_target(target)

        for projectile in self.projectiles:
            self.draw_projectile(projectile)


if __name__ == "__main__":
    ani = b2d.testbed.run(AngryShapes)
    ani
