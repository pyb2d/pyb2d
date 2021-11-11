



class RecordingRenderer(object):
    def __init__(self):
        

        self.recordings = dict()
        self.reset_recordings()


    def reset_recordings(self):
        self.recordings = dict()
        recs = self.recordings
        recs['solid_circle']    = []
        recs['circle']          = []
        recs['segment']         = []
        recs['polygon']         = []
        recs['solid_polygon']   = []
        recs['particles']       = []
        recs['soldig_polygons'] = []
        recs['polygons']        = []
        recs['segments']        = []
        recs['segments']        = []


    def draw_solid_circle(self, center, radius, axis, c):
        self.recordings['solid_circle'].append((center, radius, axis, c))

    def draw_circle(self, center, radius, c):
        self.recordings['circle'].append((center, radius, c))

    def draw_segment(self,v1, v2, c):
        self.recordings['segment'].append((v1, v2, c))

    def draw_polygon(self, vertices, c):
        self.recordings['polygon'].append((vertices, c))

    def draw_solid_polygon(self,vertices, c):
        self.recordings['solid_polygon'].append((vertices, c))

    def draw_particles(self, centers, radius,  c=None):
        self.recordings['particles'].append((centers, radius, c))

    def draw_solid_polygons(self, points, connect, c):
        self.recordings['solid_polygons'].append((points, connect, c))

    def draw_polygons(self, points, connect, c):
        self.recordings['polygons'].append((points, connect, c))

    def draw_segments(self, points, connect, c):
        self.recordings['segments'].append((points, connect, c))

    def draw_circles(self, centers, radii, c):
        self.recordings['circles'].append((points, connect, c))