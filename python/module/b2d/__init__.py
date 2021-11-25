from abc import ABC


from . _b2d import *

from . tools import *
from . extend_math import *
from . extend_draw import *
from . extend_world import *
from . extend_body import *
from . extend_fixture import *
from . extend_shapes import *
from . extend_shapes import EdgeShape
from . extend_joints import *
from . extend_collision import *
from . extend_contact import *
from . query_callback import *
if BuildConfiguration.LIQUID_FUN:
    from . extend_particles import *
# from . destruction_listener import DestructionListener





class RayCastCallback(RayCastCallbackCaller):

    def __init__(self):
        super(RayCastCallback,self).__init__(self)

    def report_fixture(self, fixture, point, normal, fraction):
        raise NotImplementedError 
    #def report_particle(self, particleSystem, index):
    #    return False
    #def should_query_particle_system(self, particleSystem):
    #    return False


class ContactListener(ContactListenerCaller):

    def __init__(self):
        super(ContactListener,self).__init__(self)

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


        


class DebugDraw(DrawCaller):
    def __init__(self, float_colors=True):
        self.float_colors = float_colors
        super(DebugDraw, self).__init__(self, bool(float_colors))

    def begin_draw(self):
        pass

    def end_draw(self):
        pass

    def draw_solid_circle(self, center, radius, axis, c):
        raise NotImplementedError 

    def draw_point(self, center, size, c):
        raise NotImplementedError 

    def draw_circle(self, center, radius, c):
        raise NotImplementedError 

    def draw_segment(self,v1, v2, c):
        raise NotImplementedError 

    def draw_polygon(self,vertices, c):
        raise NotImplementedError 

    def draw_solid_polygon(self,vertices, c):
        raise NotImplementedError 

    def draw_particles(self, centers, radius,  c=None):
        raise NotImplementedError 
    
    def draw_transform(self, xf):
        raise NotImplementedError 


class BatchDebugDrawNew(BatchDebugDrawCaller):

    def __init__(self):
        super(BatchDebugDrawNew, self).__init__(self)

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


class ContactFilter(ContactFilterCaller):

    def __init__(self):
        super(ContactFilter,self).__init__(self)


    def should_collide_fixture_fixture(self, fixtureA, fixtureB):
        pass

    def should_collide_fixture_particle(self, fixture, particleSystem, particleIndex):
        pass

    def should_collide_particle_particle(self, particleSystem, particleIndexA, particleIndexB):
        pass   



class DestructionListener(DestructionListenerCaller):

    def __init__(self):
        super(DestructionListener,self).__init__(self)

    def say_goodbye_joint(self, joint):
        pass
    def say_goodbye_fixture(self, fixture):
        pass
    def say_goodbye_particle_group(self, particleGroup):
        pass
    def say_goodbye_particle_system(self, particleSystem,index):
        pass