from . _b2d import *
from . extend_math import vec2
from . tools import _classExtender



class FooBat(object):
    pass

def fobar():
    pass




# EdgeShape = b2EdgeShape
# PolygonShape = b2PolygonShape
# CircleShape = b2CircleShape
# ChainShape = b2ChainShape
# Filter = b2Filter

# class ShapeType(object):
#     circle = Shape.ShapeType.circle
#     edge = Shape.ShapeType.edge
#     chain = Shape.ShapeType.chain
#     polygon = Shape.ShapeType.polygon

    # circle = b2Shape.ShapeType.circle
    # edge = b2Shape.ShapeType.edge
    # chain = b2Shape.ShapeType.chain
    # polygon = b2Shape.ShapeType.polygon


def shape_filter(category_bits=None, mask_bits=None, group_index=None):
    f = Filter()
    if category_bits is not None:
        f.category_bits = category_bits
    if mask_bits is not None:
        f.mask_bits = mask_bits
    if group_index is not None:
        f.group_index = group_index


# shape factories
def edge_shape(vertices):
    assert len(vertices) == 2
    s = EdgeShape()
    s.set_two_sided(vec2(vertices[0]),vec2(vertices[1]))
    return s

def chain_shape(vertices, prev_vertex=None, next_vertex=None):
    s = ChainShape()
    if  prev_vertex is None:
        prev_vertex = vertices[0]
    if  next_vertex is None:
        next_vertex = vertices[-1]

    prev_vertex = (float(prev_vertex[0]),float(prev_vertex[1]))
    next_vertex = (float(next_vertex[0]),float(next_vertex[1]))
    s.create_chain(vertices, prev_vertex, next_vertex)
    return s


def loop_shape(vertices):
    s = ChainShape()
    v = [vec2(vert) for vert in vertices]
    s.create_loop(v)


def box_loop_shape(w,h):
    verts = [
        vec2(0,0),vec2(0,w),vec2(h,w),vec2(h,0)
    ]
    return chain_shape(verts,True)

def circle_shape(radius, pos = (0,0)):
    s = CircleShape()
    s.radius = radius
    s.pos = vec2(pos)
    return s

def polygon_shape(box=None,center=(0,0),angle=0.0,vertices=None):
    s = PolygonShape()
    if vertices is None:
        s.set_as_box(box[0],box[1],center_x=center[0],center_y=center[1], angle=angle)
    else:
        verts = [ vec2(v) for v in vertices]
        s.set(verts)
    return s



def extend_polygon_shape():
    

    def _vertices(self):
        return [self.get_vertex(i) for i in range(self.vertex_count)]


    PolygonShape._vertices = _vertices
    PolygonShape.vertices = property(lambda self: self._vertices())


    # def set(self, vertices):
    #     self._set(numpy.require(vertices, requirements=['C']))
    
    # PolygonShape.vertices_setter = vertices_setter


extend_polygon_shape()
del extend_polygon_shape





class _PolygonShape(PolygonShape):

    @property
    def vertices(self):
        return [self.getVertex(i) for i in range(self.vertexCount)]

    @vertices.setter
    def vertices(self, v):
        verts = [vec2(vert) for vert in  v]
        self.set(verts)
        

_classExtender(_PolygonShape, ['vertices'])




