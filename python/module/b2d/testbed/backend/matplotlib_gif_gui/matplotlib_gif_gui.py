from ..gif_gui import GifGui

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from dataclasses import dataclass,field

matplotlib.rc('animation', html='html5')

from ..gui_base import GuiBase,list_field

class MatplotlibGifGui(GifGui):


    @dataclass
    class Settings(GifGui.Settings):
        resolution: list = list_field([400,400])
        scale: float = 10
        fps: int =  24 # we overwrite this here!
        t: float = 10.0

    def __init__(self, testbed_cls, settings, testbed_settings):
        super(MatplotlibGifGui, self).__init__(testbed_cls=testbed_cls, settings=settings, testbed_settings=testbed_settings)






    # run the world for a limited amount of steps
    def start_ui(self):
        
        self._testworld = self.testbed_cls(settings=self.testbed_settings)
        self._testworld.set_debug_draw(self.debug_draw)
        
        self._image_list = []

        def make_next_img():
            self._testworld.step(self._dt)
            self._testworld.draw_debug_data()
            ret =  self.image.copy()
            self.image[...] = 0
            return ret 


        images = [make_next_img() for _ in range(self._n)]

        fig, ax = plt.subplots()
        imshow =  plt.imshow(images[0])

        def _update_plt(num):
            imshow.set_data(images[num])
            return imshow,


        dt = self._dt
        self.ani = animation.FuncAnimation(fig, _update_plt, 
                                          frames=self._n, 
                                          interval=dt * 1000.0,
                                          blit=True, 
                                          save_count=self._n,
                                          repeat_delay=500,
                                          cache_frame_data=False)

        return self.ani

        # return self._testworld, self