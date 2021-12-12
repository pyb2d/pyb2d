import b2d
import numpy
from kivy.graphics import *
from kivy.graphics.context_instructions import *
from kivy.core.text import Label as CoreLabel
from kivy.graphics.transformation import Matrix


class KivyBatchDebugDraw(b2d.batch_debug_draw_cls(True, True, False)):

    def __init__(self, scatter,  flags=None):
        super(KivyBatchDebugDraw,self).__init__()

        self.scatter = scatter
        self.canvas = self.scatter.canvas

        # what is drawn
        if flags is None:
            flags = ['shape','joint', 'particle']#,'aabb','pair','center_of_mass','particle']
        self.flags = flags
        self.clear_flags(['shape','joint','aabb','pair','center_of_mass','particle'])
        for flag in flags:
            self.append_flags(flag)


    def _draw_solid_polygons(self, points, sizes, colors):
        n_polygons = sizes.shape[0]
        start = 0
        for i in range(n_polygons):
            s = sizes[i]
            p = points[start:start+s,:]

            v = [] 
            indices = []
            for j in range(p.shape[0]):
                v.extend([p[j,0],p[j,1],0,0])
                indices.append(j)
            Mesh(vertices=v,indices=indices,mode='triangle_fan',color=Color(*colors[i,:]))
            start += s

    def _draw_polygons(self, points, sizes, colors):
        n_polygons = sizes.shape[0]
        start = 0
        for i in range(n_polygons):
            s = sizes[i]
            p = points[start:start+s,:]

            Line(points = points, close=True, width = 1)

            start += s


    def _draw_solid_circles(self, centers, radii, axis, colors):
        n = centers.shape[0]
        for i in range(n):
            radius = radii[i]
            center = centers[i,:]-radius
            size = ([radius*2,radius*2])
            e = Ellipse(pos=center,size=size,color=Color(*colors[i,:]))
        
    def _draw_circles(self, centers, radii, colors):
        n = centers.shape[0]
        for i in range(n):
            radius = radii[i]
            Line(circle = (centers[i,0],centers[i,1], radii[i]), width = 1, color=Color(*colors[i,:]))
        

    def _draw_points(self, centers, sizes, colors):
        pass

    def _draw_segments(self, points, colors):
        n  = points.shape[0]
        for i in range(n):
            pass
            p =  points[i,0,0],points[i,0,1],points[i,1,0],points[i,1,1],
            Line(points=p, width=1.0, color=Color(*colors[i]))

    def _draw_particles(self, centers, radius, colors=None):
        default_color = (1,1,1,1)

        n_particles = centers.shape[0]
        centers -= radius
        d = 2 * radius
        size = (d, d)
        PushMatrix()
        Translate(-radius, -radius, 0)
        for i in range(n_particles):

            if colors is None:
                c = default_color
            else:
                c = colors[i,:]
            Rectangle(size=size, pos=centers[i,:],  color=Color(*c))
        PopMatrix()
    


    # non-batch api
    def draw_solid_circle(self, center, radius, axis, color):

        PushMatrix()
        Translate(-radius,-radius)
        e = Ellipse(pos=center,size=[2*radius, 2*radius],color=Color(*color))
        PopMatrix()

    def draw_circle(self, center, radius, color,line_width=1):
        Line(circle = (*center, radius), width = line_width, color=Color(*color))

    def draw_segment(self, p1, p2, color):
        Line(points=list(p1)+list(p2), width=1.0, color=Color(*color))

    def draw_polygon(self, vertices, color, line_width=1):
        Line(points = vertices, close=True, width = line_width,  color=Color(*color))

    def draw_solid_polygon(self, vertices, color):
        vertices = numpy.require(vertices)
        n_verts = vertices.shape[0]        
        v = [] 
        indices = numpy.arange(n_verts)
        for j in range(n_verts):
            v.extend([vertices[j,0],vertices[j,1],0,0])
        Mesh(vertices=v,indices=indices,mode='triangle_fan',color=Color(*color))

    # def draw_screen_text(self, position, text, size, color):
    #     PushMatrix()
    #     # matrix =  Matrix()

    #     Scale(1/self.scatter.scale)
    #     # Translate(*self.scatter.translation)
    #     t = self.scatter.transform.tolist()

    #     tx = t[3][0]
    #     ty = t[3][1]
    #     Translate(-tx,-ty)
    #     # print(tx,ty)
    #     # matrix.set(self.scatter.transform_inv)
    #     # MatrixInstruction(matrix=matrix)
    #     # print(self.scatter.transform_inv)
    #     label = CoreLabel(text=text, font_size=size)
    #     label.refresh()
    #     text = label.texture
    #     # pos = list(self.pos[i] + (self.size[i] - text.size[i]) / 2 for i in range(2))
    #     Rectangle(size=text.size, pos=position, texture=text)
    #     PopMatrix()