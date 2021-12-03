import random
import numpy
import b2d 

from .items import Destroyer, Goal
from .goos  import *

class LevelBase(object):

    @property
    def end_sensor(self):
        raise NotImplementedError


    @property
    def kill_sensors(self):
        raise NotImplementedError


class Level1(LevelBase):
    
    def __init__(self, root):
        super(Level1, self).__init__()
        self.root = root
        self.world = self.root.world

        kill_sensors_height=0.5
        gap_size = 30
        usable_size = 20
        h = 10
        end_zone_height = 3
        
        verts = [
            (0,2*h),
            (0,h),
            (usable_size,h),
            (usable_size,0),
            (usable_size+gap_size,0),
            (usable_size+gap_size,h),
            (2*usable_size+gap_size,h),
            (2*usable_size+gap_size,2*h)
        ]

        # outline of the level
        shape =  b2d.chain_shape(
            vertices=numpy.flip(verts,axis=0)
        )
        self.outline = self.world.create_static_body( position=(0, 0), shape = shape)

        # kill sensors
        shape =b2d.polygon_shape(box=(gap_size/2,kill_sensors_height/2))
        self._kill_sensor = self.world.create_static_body(
            position=(usable_size+gap_size/2, kill_sensors_height/2),
            fixtures=b2d.fixture_def(
                shape=shape,
                is_sensor=False
            ),
        )
        self._kill_sensor.user_data = Destroyer(body=self._kill_sensor)


        # end sensor
        shape =b2d.polygon_shape(box=(usable_size/2,end_zone_height/2))
        self._end_sensor = self.world.create_static_body(
            position=(1.5*usable_size+gap_size, h+end_zone_height/2),
            fixtures=b2d.fixture_def(
                shape=shape,
                is_sensor=False
            ),
        )
        self._end_sensor.user_data = Goal(body=self._end_sensor)

        # place goos
        a = AnchorGoo.create(self.root, position=(usable_size/3,h + AnchorGoo.radius))
        b = AnchorGoo.create(self.root, position=(usable_size*2/3,h + AnchorGoo.radius))
        c = PlainGoo.create(self.root, position=(usable_size*1/2,h + PlainGoo.radius + 3))

        j = connect_goos(self.root, a,b)
        j = connect_goos(self.root, a,c)
        j = connect_goos(self.root, b,c)

