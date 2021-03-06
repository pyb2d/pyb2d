import b2d
from collections import defaultdict


class RecMixIn(object):
    def __init__(self):
        self.recordings = defaultdict(list)

    def total_calls(self):
        l = 0
        for k, v in self.recordings.items():
            l += len(v)
        return l


class RecDestructionListener(b2d.DestructionListener, RecMixIn):
    def __init__(self):
        b2d.DestructionListener.__init__(self)

        RecMixIn.__init__(self)

    def say_goodbye_joint(self, joint):
        self.recordings["say_goodbye_joint"].append(dict(joint=joint))

    def say_goodbye_fixture(self, fixture):
        self.recordings["say_goodbye_fixture"].append(dict(fixture=fixture))

    def say_goodbye_particle_group(self, particleGroup):
        self.recordings["say_goodbye_particle_group"].append(
            dict(particleGroup=particleGroup)
        )

    def say_goodbye_particle_system(self, particleSystem, index):
        self.recordings["say_goodbye_particle_system"].append(
            dict(particleSystem=particleSystem, index=index)
        )


class RecContactListener(b2d.ContactListener, RecMixIn):
    def __init__(self):
        b2d.ContactListener.__init__(self)
        RecMixIn.__init__(self)

    def begin_contact(self, contact):
        self.recordings["begin_contact"].append(dict(contact=contact))

    def end_contact(self, contact):
        self.recordings["end_contact"].append(dict(contact=contact))

    def begin_contact_particle_body(self, particleSystem, particleBodyContact):
        self.recordings["begin_contact_particle_body"].append(
            dict(particleSystem=particleSystem, particleBodyContact=particleBodyContact)
        )

    def begin_contact_particle(self, particleSystem, indexA, indexB):
        self.recordings["begin_contact_particle"].append(
            dict(particleSystem=particleSystem, indexA=indexA, indexB=indexB)
        )

    def end_contact_particle(self, particleSystem, indexA, indexB):
        self.recordings["end_contact_particle"].append(
            dict(particleSystem=particleSystem, indexA=indexA, indexB=indexB)
        )

    def pre_solve(self, contact, oldManifold):
        self.recordings["pre_solve"].append(
            dict(contact=contact, oldManifold=oldManifold)
        )

    def post_solve(self, contact, impulse):
        self.recordings["post_solve"].append(dict(contact=contact, impulse=impulse))


class RecContactFilter(b2d.ContactFilter, RecMixIn):
    def __init__(self):
        b2d.ContactFilter.__init__(self)
        RecMixIn.__init__(self)

    def should_collide_fixture_fixture(self, fixtureA, fixtureB):
        self.recordings["should_collide_fixture_fixture"].append(
            dict(fixtureA=fixtureA, fixtureB=fixtureA)
        )

    def should_collide_fixture_particle(self, fixture, particleSystem, particleIndex):
        self.recordings["should_collide_fixture_particle"].append(
            dict(particleSystem=particleSystem, particleIndex=particleIndex)
        )

    def should_collide_particle_particle(
        self, particleSystem, particleIndexA, particleIndexB
    ):
        self.recordings["should_collide_particle_particle"].append(
            dict(particleIndexA=particleIndexA, particleIndexB=particleIndexA)
        )


_batch_debug_draw_base_cls = b2d.batch_debug_draw_cls(False, False, True)


class RecBatchDebugDraw(_batch_debug_draw_base_cls, RecMixIn):
    def __init__(self):
        _batch_debug_draw_base_cls.__init__(self)
        RecMixIn.__init__(self)

        flags = ["shape", "joint", "aabb", "pair", "center_of_mass", "particle"]
        self.clear_flags(flags)
        for flag in flags:
            self.append_flags(flag)

    def _draw_solid_polygons(self, points, sizes, colors):
        self.recordings["draw_solid_polygons"].append(
            dict(points=points, sizes=sizes, colors=colors)
        )

    def _draw_polygons(self, points, sizes, colors):
        self.recordings["draw_polygons"].append(
            dict(points=points, sizes=sizes, colors=colors)
        )

    def _draw_segments(self, points, colors):
        self.recordings["draw_segments"].append(dict(points=points, colors=colors))

    def _draw_solid_circles(self, centers, radii, axis, colors):
        self.recordings["draw_solid_circles"].append(
            dict(centers=centers, radii=radii, axis=axis, colors=colors)
        )

    def _draw_circles(self, centers, radii, colors):
        self.recordings["draw_circles"].append(
            dict(centers=centers, radii=radii, colors=colors)
        )

    def _draw_points(self, centers, sizes, colors):
        self.recordings["draw_points"].append(
            dict(centers=centers, sizes=sizes, colors=colors)
        )

    def _draw_particles(self, centers, radius, colors):
        self.recordings["draw_particles"].append(
            dict(centers=centers, radius=radius, colors=colors)
        )
