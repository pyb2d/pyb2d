import numpy
import b2d as b2
import pygame
import pygame.locals 
from skimage.morphology import disk, binary_dilation

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
        pygame.draw.polygon(self.surface, c, vertices, 1)

    def draw_solid_polygon(self,vertices, c):
        pygame.draw.polygon(self.surface, c, vertices, 0)

    def draw_particles(self, centers, radius,  c=None):
        if c is None:
            c = (0,255,255)
        for i in range(centers.shape[0]):
            x,y = centers[i,:]
            if(numpy.isnan(x) or numpy.isnan(y)):
                    continue
            pygame.draw.circle(self.surface, c, (x,y), radius, 0)
        if False:
            shape = self.surface.get_size()
            # print("surface size ",shape)

            surf = pygame.Surface( [int(s) for s in shape], flags=pygame.SRCALPHA)

            alpha_view = pygame.surfarray.pixels_alpha(surf)
            pixels_2d = pygame.surfarray.pixels3d(surf)



            # print(centers.shape, centers.min(), centers.max())
            cx = centers[:,0].astype('uint32')
            cy = centers[:,1].astype('uint32')

            pixels_2d[...] = 255


            if c is None:
                c = (0,255,255)
            centers -= radius
            d = radius * 2
            for i in range(centers.shape[0]):
                x,y = centers[i,:]
                if(numpy.isnan(x) or numpy.isnan(y)):
                    continue
                x,y = int(x),int(y)
                if x >= 0.0 and x < shape[0] and  y >= 0.0 and y < shape[1]:
                    alpha_view[x,y] = 255
                # \\pygame.draw.circle(self.surface, c, ,radius, 0)

            # binary_dilation(alpha_view, disk(int(radius+0.5), dtype=bool), out=alpha_view)
            del pixels_2d
            del alpha_view
            self.surface.blit(surf, (0, 0))


            # pygame.draw.rect(self.surface, c, (
            #         centers[i,0],
            #         centers[i,1],
            #         d,d
            #     ),0)

    def draw_transform(self, t):
        pass