"""
Billiard
===========================

This example shows how to implement a very simple Billiard game with Box2D
"""


from b2d.testbed import TestbedBase
import random
import numpy
import b2d
import math
import random


class Billiard(TestbedBase):

    name = "Billiard"

    def __init__(self, settings=None):
        super(Billiard, self).__init__(gravity=(0, 0), settings=settings)
        dimensions = [30, 50]
        self.dimensions = dimensions

        # the outer box
        box_shape = b2d.ChainShape()
        box_shape.create_loop(
            [
                (0, 0),
                (0, dimensions[1]),
                (dimensions[0], dimensions[1]),
                (dimensions[0], 0),
            ]
        )
        self.ball_radius = 1
        box = self.world.create_static_body(
            position=(0, 0), fixtures=b2d.fixture_def(shape=box_shape, friction=0)
        )

        self.place_balls()
        self.place_pockets()

        # mouse interaction
        self._selected_ball = None
        self._selected_ball_pos = None
        self._last_pos = None

        # balls to be destroyed in the next step
        # since they are in the pocket
        self._to_be_destroyed = []

    def place_pockets(self):
        pocket_radius = 1
        self.pockets = []

        def place_pocket(position):
            pocket_shape = b2d.circle_shape(radius=pocket_radius / 3)
            pocket = self.world.create_static_body(
                position=position,
                fixtures=b2d.fixture_def(shape=pocket_shape, is_sensor=True),
                user_data=("pocket", None),
            )
            self.pockets.append(pocket)

        d = pocket_radius / 2

        place_pocket(position=(0 + d, 0 + d))
        place_pocket(position=(self.dimensions[0] - d, 0 + d))

        place_pocket(position=(0 + d, self.dimensions[1] / 2))
        place_pocket(position=(self.dimensions[0] - d, self.dimensions[1] / 2))

        place_pocket(position=(0 + d, self.dimensions[1] - d))
        place_pocket(position=(self.dimensions[0] - d, self.dimensions[1] - d))

    def place_balls(self):
        self.balls = []

        base_colors = [
            (1, 1, 0),
            (0, 0, 1),
            (1, 0, 0),
            (1, 0, 1),
            (1, 0.6, 0),
            (0, 1, 0),
            (0.7, 0.4, 0.4),
        ]
        colors = []
        for color in base_colors:
            # ``full`` ball
            colors.append((color, color))
            # ``half`` ball (half white)
            colors.append((color, (1, 1, 1)))

        random.shuffle(colors)
        colors.insert(4, ((0, 0, 0), (0, 0, 0)))  # black

        n_y = 5
        c_x = self.dimensions[0] / 2
        diameter = (self.ball_radius * 2) * 1.01

        bi = 0
        for y in range(n_y):

            py = y * diameter * 0.5 * math.sqrt(3)
            n_x = y + 1
            ox = diameter * (n_y - y) / 2
            for x in range(y + 1):
                position = (x * diameter + 10 + ox, py + 30)
                self.create_billard_ball(position=position, color=colors[bi])
                bi += 1

        self.create_billard_ball(position=(c_x, 10), color=((1, 1, 1), (1, 1, 1)))

    def create_billard_ball(self, position, color):

        ball = self.world.create_dynamic_body(
            position=position,
            fixtures=b2d.fixture_def(
                shape=b2d.circle_shape(radius=self.ball_radius),
                density=1.0,
                restitution=0.8,
            ),
            linear_damping=0.4,
            user_data=("ball", color),
            fixed_rotation=True,
        )
        self.balls.append(ball)

    def begin_contact(self, contact):
        body_a = contact.body_a
        body_b = contact.body_b

        ud_a = body_a.user_data
        ud_b = body_b.user_data
        if ud_a is None or ud_b is None:
            return

        if ud_b[0] == "ball":
            body_a, body_b = body_b, body_a
            ud_a, ud_b = ud_b, ud_a

        if ud_a[0] == "ball" and ud_b[0] == "pocket":
            self._to_be_destroyed.append(body_a)

    def pre_step(self, dt):
        for b in self._to_be_destroyed:
            self.balls.remove(b)
            self.world.destroy_body(b)
        self._to_be_destroyed = []

    def ball_at_position(self, pos):
        body = self.world.find_body(pos)
        if body is not None:
            user_data = body.user_data
            if user_data is not None and user_data[0] == "ball":
                return body
        return None

    def on_mouse_down(self, pos):
        body = self.ball_at_position(pos)
        if body is not None:
            self._selected_ball = body
            self._selected_ball_pos = pos
            return True

        return False

    def on_mouse_move(self, pos):
        if self._selected_ball is not None:
            self._last_pos = pos
        return False

    def on_mouse_up(self, pos):
        if self._selected_ball is not None:
            self._last_pos = pos
            # if the mouse is in the starting ball itself we do nothing
            if self.ball_at_position(pos) != self._selected_ball:
                delta = b2d.vec2(self._selected_ball_pos) - b2d.vec2(self._last_pos)
                delta *= 100.0
                self._selected_ball.apply_linear_impulse(
                    delta, self._selected_ball_pos, True
                )
        self._selected_ball = None
        self._selected_ball_pos = None
        self._last_pos = None
        return False

    def post_debug_draw(self):

        for pocket in self.pockets:
            self.debug_draw.draw_solid_circle(
                pocket.position, self.ball_radius, (1, 0), (1, 1, 1)
            )

        for ball in self.balls:
            _, (color0, color1) = ball.user_data

            self.debug_draw.draw_solid_circle(
                ball.position, self.ball_radius, (1, 0), color0
            )
            self.debug_draw.draw_solid_circle(
                ball.position, self.ball_radius / 2, (1, 0), color1
            )
            self.debug_draw.draw_circle(
                ball.position, self.ball_radius, (1, 1, 1), line_width=0.1
            )

        if self._selected_ball is not None:

            # draw circle around selected ball
            self.debug_draw.draw_circle(
                self._selected_ball.position,
                self.ball_radius * 2,
                (1, 1, 1),
                line_width=0.2,
            )

            # mark position on selected ball with red dot
            self.debug_draw.draw_solid_circle(
                self._selected_ball_pos, self.ball_radius * 0.2, (1, 0), (1, 0, 0)
            )

            # draw the line between marked pos on ball and last pos
            if self._last_pos is not None:
                self.debug_draw.draw_segment(
                    self._selected_ball_pos, self._last_pos, (1, 1, 1), line_width=0.2
                )


if __name__ == "__main__":
    ani = b2d.testbed.run(Billiard)
    ani
