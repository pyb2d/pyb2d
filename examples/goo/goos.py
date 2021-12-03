
from b2d.testbed import TestbedBase
import random
import numpy as np
import b2d 
import networkx
from functools import partial
# from abc import ABC,abstractmethod

from .utils import *
from .query import *

from enum import Enum






def query_goo_placement(root, pos):
    def filter_func(bdy):
        goo = bdy.user_data
        if isinstance(goo, GooBase) and \
           goo.can_connect_with_cls(root.goo_cls) and \
           goo.has_free_connection():
           return True
        return False
    bodies = bodies_in_radius(root.world, pos=pos, radius=root.goo_cls.discover_radius,
                                filter_func=filter_func, max_elements=10)
    goos = [b.user_data for b in bodies]
    n_goos = len(goos)

    
    if n_goos >= 2:

        # insert as joint?
        def distance(a,b, p):
            if root.goo_graph.has_edge(a[0], b[0]):
                return float('inf')
            return  np.linalg.norm((a[1] + b[1])/2 - p)

        i,j,best_dist = best_pairwise_distance(goos, 
            f= lambda goo: (goo,np.array(goo.body.position)),
            distance=partial(distance, p=pos))

        if best_dist < 0.5:
            return InsertInfo(InsertType.AS_JOINT,
                goo_a=goos[i], goo_b=goos[j])     
    
        # insert as body?
        f = lambda goo :  (goo, (goo.body.position- b2d.vec2(pos)).length)

        def distance(a,b):
            if not root.goo_graph.has_edge(a[0], b[0]):
                return float('inf')
            return (a[1] + b[1])

        i,j,best_dist = best_pairwise_distance(goos, f=f, distance=distance)

        if best_dist < 10:
            return InsertInfo(InsertType.AS_GOO, goo_a= goos[i], goo_b= goos[j])

    return InsertInfo(InsertType.CANNOT_INSERT)








class InsertType(Enum):
    AS_GOO = 1
    AS_JOINT = 2
    CANNOT_INSERT = 3


class InsertInfo(object):
    def __init__(self, insert_type, **info):
        self.insert_type = insert_type
        self.info = info

class GooBase(object):
    discover_radius = 8
    max_degree = 8
    min_degree = 2

    def __init__(self, root, body):
        self.root = root
        self.body = body


    @classmethod
    def can_connect_with_cls(cls, other_cls):
        return True

    @property
    def degree(self):
        return self.root.goo_graph.degree(self)

    def has_free_connection(self):
        d = self.degree
        return d >= self.min_degree and d < self.max_degree

class AnchorGoo(GooBase):
    radius = 0.75
    density = 100
    @staticmethod
    def create(root, position):
        world = root.world

        shape = b2d.polygon_shape(box=[AnchorGoo.radius,AnchorGoo.radius])
        fixture = b2d.fixture_def(shape=shape, density=AnchorGoo.density, friction=0.2)
        body = world.create_dynamic_body(
            position=position, 
            fixtures=fixture,
            linear_damping=0.2,
            angular_damping=0.9
        )
        goo = AnchorGoo(root, body)
        body.user_data = goo
        root.goo_graph.add_node(goo)
        return goo

    def __init__(self, root, body):
        super(AnchorGoo, self).__init__(root=root, body=body)

class PlainGoo(GooBase):

    radius = 0.75

    @staticmethod
    def draw_tentative(root, position, insert_info):
        insert_type = insert_info.insert_type
        if insert_type == InsertType.CANNOT_INSERT:
            color = (1,0,0)
        elif insert_type == InsertType.AS_GOO:
    
            root.debug_draw.draw_circle(
                position,
                PlainGoo.radius,
                (0,1,0)
            )
            root.debug_draw.draw_segment(
                position, insert_info.info['goo_a'].body.position, (0,1,0)
            )
            root.debug_draw.draw_segment(
                position, insert_info.info['goo_b'].body.position, (0,1,0)
            )

        elif insert_type == InsertType.AS_JOINT:
            root.debug_draw.draw_segment(
                insert_info.info['goo_a'].body.position, 
                insert_info.info['goo_b'].body.position, (0,1,0)
            )

        
    @staticmethod
    def create(root, position):
        world = root.world

        shape = b2d.circle_shape(radius=PlainGoo.radius)
        fixture = b2d.fixture_def(shape=shape, density=1, friction=0.2)
        body = world.create_dynamic_body(
            position=position, 
            fixtures=fixture,
            linear_damping=0.2,
            angular_damping=0.9
        )
        goo = PlainGoo(root, body)
        root.goo_graph.add_node(goo)
        body.user_data = goo

        return goo

    def __init__(self, root, body):
        super(PlainGoo, self).__init__(root=root, body=body)



def connect_goos(root, goo_a, goo_b):
    graph = root.goo_graph
    world = root.world
    body_a = goo_a.body
    body_b = goo_b.body

    length = (body_a.position - body_b.position).length

    j =  world.create_distance_joint(body_a,body_b, 
        length=length,
        stiffness=300
    )
    graph.add_edge(goo_a, goo_b,joint=j)
    return j