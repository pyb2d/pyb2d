import random
import numpy
import b2d 
import networkx



class _BodiesInAABBCallback(b2d.QueryCallback):
    def __init__(self, max_elements = float('inf'), filter_func=None):
        super(_BodiesInAABBCallback,self).__init__()

        if filter_func is None:
            filter_func = lambda bdy:True
        self.filter_func = filter_func
        self.max_elements = max_elements
        self.bodies = set()
    def report_fixture(self, fixture):
        body = fixture.body
        if body not in self.bodies:
            if self.filter_func(body):
                self.bodies.add(body)
                if len(self.bodies) >= self.max_elements:
                    return False
        return True


def bodies_in_aabb(world, pos, radius, max_elements = float('inf'), filter_func=None):
    if filter_func is None:
        filter_func = lambda bdy:True

    pos = b2d.vec2(pos)
    box =  b2d.aabb(lower_bound=pos - b2d.vec2(radius, radius),
                    upper_bound=pos + b2d.vec2(radius, radius))
    query = _BodiesInAABBCallback(max_elements=max_elements, filter_func=filter_func)
    world.query_aabb(query, box)
    return query.bodies


def bodies_in_radius(world, pos, radius, max_elements = float('inf'), filter_func=None):
    if filter_func is None:
        filter_func = lambda bdy:True

    def _filter_func(body):
        if filter_func(body):
            return (body.position - b2d.vec2(pos)).length <= radius
        return False
    return bodies_in_aabb(world=world, pos=pos, radius=radius, max_elements=max_elements, filter_func=_filter_func)


