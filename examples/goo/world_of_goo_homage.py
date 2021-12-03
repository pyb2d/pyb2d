"""
Goo
===========================

A world of goo homage
"""

from b2d.testbed import TestbedBase
import random
import numpy
import b2d 
import networkx
from functools import partial
# from abc import ABC,abstractmethod

from .utils    import *
from .level    import *
from .goos     import *
from .query    import *
from .geometry import *



class WorldOfGooHomage(TestbedBase):

    name = "Function Shape"
    
    def __init__(self): 
        super(WorldOfGooHomage, self).__init__()
        

        self.goo_graph = networkx.Graph()

        # level related
        self.level = Level1(root=self)

        # mouse related
        self._mouse_is_down = False
        self._last_pos = None
        self._handled_click = False
        
        # the current goo to place
        self.goo_cls = PlainGoo
        self._insert_info = InsertInfo(InsertType.CANNOT_INSERT)

        # goo-s do be destroyed in the next step
        self.marked_for_destruction = []

 
    def on_mouse_down(self, pos):
        print("goo on_mouse_down")
        self._mouse_is_down = True
        self._last_pos = pos
        self._insert_info = query_goo_placement(self, pos)
        handled = False
        if self._insert_info.insert_type == InsertType.CANNOT_INSERT:
            self._handled_click = False
            return super(WorldOfGooHomage, self).on_mouse_down(pos)
        else:
            self._handled_click = True
            return True

    def on_mouse_move(self, pos):
        handled = False
        self._last_pos = pos
        if self._mouse_is_down:
           self._insert_info = query_goo_placement(self, pos)
        handled = False
        if not self._handled_click:
            return super(WorldOfGooHomage, self).on_mouse_move(pos)
        else:
            return True

    def on_mouse_up(self, pos):
        self._mouse_is_down = False
        self._insert_info = query_goo_placement(self, pos)
        if self._insert_info.insert_type == InsertType.AS_GOO:

            goo = self.goo_cls.create(self, position=pos)
            goo_a = self._insert_info.info['goo_a']
            goo_b = self._insert_info.info['goo_b']
            # connect_goo_tripple(self, goo_a, goo_b, goo_new=goo)
            connect_goos(self, goo, goo_a)
            connect_goos(self, goo, goo_b)
        elif self._insert_info.insert_type == InsertType.AS_JOINT:
            goo_a = self._insert_info.info['goo_a']
            goo_b = self._insert_info.info['goo_b']
            connect_goos(self, goo_b, goo_a)

        self._insert_info = InsertType.CANNOT_INSERT
        self._last_pos = pos
        handled = False
        if not self._handled_click:
            return super(WorldOfGooHomage, self).on_mouse_up(pos)
        else:
            self._handled_click = False
            return True

    def begin_contact(self, contact):
        user_data_a = contact.body_a.user_data
        user_data_b = contact.body_b.user_data
        a_is_goo =  isinstance(user_data_a, GooBase)
        b_is_goo =  isinstance(user_data_b, GooBase)

        if xor(a_is_goo, b_is_goo):
            if a_is_goo:
                self.begin_goo_contact(user_data_a, user_data_b)
            else:
                self.begin_goo_contact(user_data_b, user_data_a)



    def begin_goo_contact(self, goo, other):
        if isinstance(other, Destroyer):
            self.marked_for_destruction.append(goo)

    def pre_step(self, dt):


        for goo in self.marked_for_destruction:
            self.goo_graph.remove_node(goo)
            self.world.destroy_body(goo.body)
        self.marked_for_destruction = []

    def post_debug_draw(self):
        
        if self._mouse_is_down and  self._last_pos is not None:

            self.goo_cls.draw_tentative(self, self._last_pos, 
                insert_info=self._insert_info)



if __name__ == "__main__":
        
    ani = b2d.testbed.run(WorldOfGooHomage)
    ani