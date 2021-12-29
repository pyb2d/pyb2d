import b2d

from .common import *
from .callbacks import *
import pytest
import numpy as np


@pytest.fixture
def many_body_world(world):

    circle_fixture = b2d.fixture_def(
        shape=b2d.circle_shape(radius=0.25), density=1, friction=0.5
    )

    for x in range(10):
        for y in range(10):

            body = world.create_dynamic_body(
                position=(x, y),
                fixtures=circle_fixture,
                angular_damping=0.5,
                linear_damping=0.5,
            )
    return world


@pytest.fixture
def many_body_world_and_body_vector(many_body_world):

    body_vector = b2d.BodyVector()
    body_list = []
    for body in many_body_world.bodies:
        body_vector.append(body)
        body_list.append(body)
    assert len(body_vector) == len(body_list)
    assert len(body_vector) == 100
    return many_body_world, body_vector, body_list


class TestBodyVector(object):
    def test_batch_api(self, many_body_world_and_body_vector):

        world, body_vector, body_list = many_body_world_and_body_vector

        # position
        position = body_vector.position()
        should_position = np.array([b.position for b in body_list], dtype="float32")
        assert np.allclose(position, should_position)

        # world_center
        world_center = body_vector.world_center()
        should_world_center = np.array(
            [b.world_center for b in body_list], dtype="float32"
        )
        assert np.allclose(world_center, should_world_center)

        # local_center
        local_center = body_vector.local_center()
        should_local_center = np.array(
            [b.local_center for b in body_list], dtype="float32"
        )
        assert np.allclose(local_center, should_local_center)

        # angle
        angle = body_vector.angle()
        should_angle = np.array([b.angle for b in body_list], dtype="float32")
        assert np.allclose(angle, should_angle)

        # angle
        angle = body_vector.angle()
        should_angle = np.array([b.angle for b in body_list], dtype="float32")
        assert np.allclose(angle, should_angle)

        # mass
        mass = body_vector.mass()
        should_mass = np.array([b.mass for b in body_list], dtype="float32")
        assert np.allclose(mass, should_mass)

        # inertia
        inertia = body_vector.inertia()
        should_inertia = np.array([b.inertia for b in body_list], dtype="float32")
        assert np.allclose(inertia, should_inertia)

        # linear_damping
        linear_damping = body_vector.linear_damping()
        should_linear_damping = np.array(
            [b.linear_damping for b in body_list], dtype="float32"
        )
        assert np.allclose(linear_damping, should_linear_damping)

        # angular_damping
        angular_damping = body_vector.angular_damping()
        should_angular_damping = np.array(
            [b.angular_damping for b in body_list], dtype="float32"
        )
        assert np.allclose(angular_damping, should_angular_damping)

        # bullet
        bullet = body_vector.bullet()
        should_bullet = np.array([b.bullet for b in body_list], dtype="bool")
        assert np.allclose(bullet, should_bullet)

        # sleeping_allowed
        sleeping_allowed = body_vector.sleeping_allowed()
        should_sleeping_allowed = np.array(
            [b.sleeping_allowed for b in body_list], dtype="bool"
        )
        assert np.allclose(sleeping_allowed, should_sleeping_allowed)

        # awake
        awake = body_vector.awake()
        should_awake = np.array([b.awake for b in body_list], dtype="bool")
        assert np.allclose(awake, should_awake)

        # enabled
        enabled = body_vector.enabled()
        should_enabled = np.array([b.enabled for b in body_list], dtype="bool")
        assert np.allclose(enabled, should_enabled)

        # fixed_rotation
        fixed_rotation = body_vector.fixed_rotation()
        should_fixed_rotation = np.array(
            [b.fixed_rotation for b in body_list], dtype="bool"
        )
        assert np.allclose(fixed_rotation, should_fixed_rotation)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main())
