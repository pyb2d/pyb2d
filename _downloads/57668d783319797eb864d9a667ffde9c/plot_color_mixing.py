"""
Color Mixing
===========================

This example show how to create particles which mix colors when they touch
"""

from b2d.testbed import TestbedBase
import random
import numpy
import b2d


class ColorMixing(TestbedBase):

    name = "ColorMixing"

    def __init__(self, settings=None):
        super(ColorMixing, self).__init__(settings=settings)
        dimensions = [30, 30]

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
        box = self.world.create_static_body(position=(0, 0), shape=box_shape)

        fixtureA = b2d.fixture_def(
            shape=b2d.circle_shape(1), density=2.2, friction=0.2, restitution=0.5
        )
        body = self.world.create_dynamic_body(position=(13, 10), fixtures=fixtureA)

        pdef = b2d.particle_system_def(
            viscous_strength=0.9,
            spring_strength=0.0,
            damping_strength=0.5,
            pressure_strength=0.5,
            color_mixing_strength=0.008,
            density=2,
        )
        psystem = self.world.create_particle_system(pdef)
        psystem.radius = 0.3
        psystem.damping = 1.0

        colors = [
            (255, 0, 0, 255),
            (0, 255, 0, 255),
            (0, 0, 255, 255),
            (255, 255, 0, 255),
        ]
        posiitons = [(6, 10), (20, 10), (20, 20), (6, 20)]
        for color, pos in zip(colors, posiitons):

            shape = b2d.polygon_shape(box=(5, 5), center=pos, angle=0)
            pgDef = b2d.particle_group_def(
                flags=b2d.ParticleFlag.waterParticle
                | b2d.ParticleFlag.colorMixingParticle,
                # group_flags=b2d.ParticleGroupFlag.solidParticleGroup,
                shape=shape,
                strength=1.0,
                color=color,
            )
            group = psystem.create_particle_group(pgDef)


if __name__ == "__main__":

    ani = b2d.testbed.run(ColorMixing)
    ani
