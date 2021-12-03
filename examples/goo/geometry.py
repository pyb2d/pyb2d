import numpy as np


def point_line_distance(line, point):
    return np.linalg.norm(np.cross(line[1]-line[0], line[0]-point))/np.linalg.norm(line[1]-line[0])
