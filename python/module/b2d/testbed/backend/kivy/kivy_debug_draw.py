import b2d
import numpy
from kivy.graphics import *


# class CanvasDraw(object):    
#     def __init__(self):
#         pass

#     def draw_solid_circle(self, center, radius, axis, color):
#         center = (numpy.array(center)-radius)
#         size = numpy.array([radius*2,radius*2])
#         #print "color",color
#         #with self.canvas:
#         e = Ellipse(pos=center,size=size,color=Color(*color))

#     def draw_segment(self,v1, v2, color):
#         #v1 = (numpy.array(v1)+self.offset)*self.scale
#         #v2 = (numpy.array(v2)+self.offset)*self.scale
#         #with self.canvas:
#         Line(points=[v1[0],v1[1],v2[0],v2[1]], width=1.0, color=Color(*color))

#     def draw_solid_polygon(self,vertices, color):
#         vertices = numpy.array(vertices)
#         vertices[:,0] #+= self.offset[0]
#         vertices[:,1] #+= self.offset[1]
#         #vertices*=self.scale

#         assert vertices.shape[0] ==vertexCount

#         v = [] 
#         indices = []
#         for i in range(vertices.shape[0]):
#             v.extend([vertices[i,0],vertices[i,1],0,0])
#             indices.append(i)
#         #with self.canvas:
#         Mesh(vertices=v,indices=indices,mode='triangle_fan',color=Color(*color))




class KivyBatchDebugDraw(b2d.BatchDebugDrawNew):

    def __init__(self, flags=None):
        super(KivyBatchDebugDraw,self).__init__()

        # what is drawn
        if flags is None:
            flags = ['shape','joint']#,'aabb','pair','center_of_mass','particle']
        self.flags = flags
        self.clear_flags(['shape','joint','aabb','pair','center_of_mass','particle'])
        for flag in flags:
            self.append_flags(flag)


    def draw_solid_polygons(self, points, sizes, colors):
        self._draw_polygons(points, sizes, colors, 0)

    def draw_polygons(self, points, sizes, colors):
        self._draw_polygons(points, sizes, colors, 1)

    def _draw_polygons(self, points, sizes, colors, lw):



#         v = [] 
#         indices = []
#         for i in range(vertices.shape[0]):
#             v.extend([vertices[i,0],vertices[i,1],0,0])
#             indices.append(i)
#         #with self.canvas:
#         Mesh(vertices=v,indices=indices,mode='triangle_fan',color=Color(*color))

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
            #with self.canvas:
            Mesh(vertices=v,indices=indices,mode='triangle_fan',color=Color(*colors[i,:]/255.0))



            # pygame.draw.polygon(self._surface, colors[i,:], p, lw)
            start += s


    def draw_solid_circles(self, centers, radii, axis, colors):
        self._draw_circles(centers, radii, colors, lw=0)
        
    def draw_circles(self, centers, radii, colors):
        self._draw_circles(centers, radii, colors, lw=1)

    def _draw_circles(self, centers, radii,  colors, lw):
        # print("draw")
        n = centers.shape[0]
        for i in range(n):
            radius = radii[i]
            center = centers[i,:]-radius
            size = ([radius*2,radius*2])
            e = Ellipse(pos=center,size=size,color=Color(*colors[i,:]/255.0))
            # pygame.draw.circle(self._surface, 
            #     colors[i,:], 
            #     centers[i,:],
            #     radii[i], 
            #     lw)

    def draw_points(self, centers, sizes, colors):
        pass

    def draw_segments(self, points, colors):
        n  = points.shape[0]
        for i in range(n):
            pass
            # pygame.draw.line(
            #     self._surface,
            #     colors[i,:],
            #     points[i,0,:],
            #     points[i,1,:]
            # )
            p =  points[i,0,0],points[i,0,1],points[i,1,0],points[i,1,1],
            Line(points=p, width=1.0, color=Color(*colors[i]/255.0))

    def draw_particles(self, centers, radius, colors=None):
        default_color = (255,255,255,255)

        n_particles = centers.shape[0]
        centers -= radius
        d = 2 * radius
        for i in range(n_particles):

            if colors is None:
                c = default_color
            else:
                c = colors[i,:]

            # pygame.draw.rect(
            #     self._surface, c,
            #     (centers[i,0], centers[i,1], d, d)
            # )

