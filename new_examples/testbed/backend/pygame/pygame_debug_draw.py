import numpy
import pybox2d as b2
import pygame
import pygame.locals 

class PygameDebugDraw(b2.DebugDraw):
    def __init__(self, surface):
        super(PygameDebugDraw, self).__init__(float_colors=False)
        self.surface = surface
        self.axis_color = (20,20,20)

    def draw_solid_circle(self, center, radius, axis, color):
        pygame.draw.circle(self.surface, color, center,radius, 0)

        pygame.draw.aaline(self.surface, self.axis_color, center,
                           (center[0] - radius * axis[0],
                            center[1] + radius * axis[1]))

    def draw_point(self, center, size, c):
        pygame.draw.circle(self.surface, c, center,size/2.0, 1)

    def draw_circle(self, center, radius, c):
        pygame.draw.circle(self.surface, c, center,radius, 1)


    def draw_segment(self,v1, v2, c):
        pygame.draw.aaline(self.surface, c, v1, v2, 1)

    def draw_polygon(self,vertices, c):
        print(vertices.shape, vertices)
        pygame.draw.polygon(self.surface, c, vertices, 1)


    def draw_solid_polygon(self,vertices, c):
        pygame.draw.polygon(self.surface, c, vertices, 0)

    def draw_particles(self, centers, radius,  c=None):
        pass    
    def draw_transform(self, t):
        pass