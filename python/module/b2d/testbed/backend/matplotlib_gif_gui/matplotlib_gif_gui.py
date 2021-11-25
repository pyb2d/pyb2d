from ..gif_gui import GifGui

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class MatplotlibGifGui(GifGui):
    def __init__(self, *args, **kwargs):
        super(MatplotlibGifGui, self).__init__(*args, **kwargs)







    # run the world for a limited amount of steps
    def start_ui(self):
        
        self._testworld = self.testbed_cls(**self.testbed_kwargs)
        self._testworld.world.set_debug_draw(self.debug_draw)
        
        self._image_list = []

        for i in range(self._n):
            self._testworld.step(self._dt)
            self._testworld.world.draw_debug_data()


            self._image_list.append(self.image.copy())
            self.image[...] = 0


        fig, ax = plt.subplots()
        imshow =  ax.imshow(self._image_list[0])

        def _update_plt(num):
            print("update", num)
            imshow.set_data(self._image_list[num])
            return imshow,


        dt = self._dt
        self.ani = animation.FuncAnimation(fig, _update_plt, len(self._image_list), interval=dt, blit=True)

        # plt.show()

        return self._testworld, self