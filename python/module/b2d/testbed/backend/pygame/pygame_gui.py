import numpy
import b2d as b2
import pygame
import pygame.locals
import time

from ..gui_base import GuiBase
from .pygame_debug_draw import PyGameBatchDebugDraw


class PygameGui(GuiBase):
    class Settings(GuiBase.Settings):
        pass

    def __init__(self, testbed_cls, settings, testbed_settings):

        # settings
        self.settings = settings

        # testworld
        self.testbed_settings = testbed_settings
        self.testbed_cls = testbed_cls
        self._testworld = None

        # flag to stop loop
        self._exit = False

        # surface
        self._surface = None

        # mouse state
        self._last_was_drag = False
        self._last_pos = None
        self._handle_click = False

        # steping settings
        self._fps = settings.fps
        self._dt_s = 1.0 / self._fps

    def make_testworld(self):

        if self._testworld is not None:
            self._testworld.say_goodbye_world()
        self._testworld = self.testbed_cls(settings=self.testbed_settings)

    def start_ui(self):

        # make the world
        self.make_testworld()

        # Initialise screen
        pygame.init()
        self._surface = pygame.display.set_mode(self.settings.resolution)
        pygame.display.set_caption(self.testbed_cls.name)

        # debug draw
        # self.debug_draw = PygameDebugDraw(surface=self._surface)
        self.debug_draw = PyGameBatchDebugDraw(surface=self._surface)
        self.debug_draw.screen_size = self.settings.resolution
        self.debug_draw.flip_y = True
        self.debug_draw.scale = self.settings.scale
        self.debug_draw.translate = self.settings.translate
        self.debug_draw.append_flags(
            [
                "shape",
                "joint",
                # 'aabb',
                # 'pair',
                "center_of_mass",
                "particle",
            ]
        )
        self._testworld.set_debug_draw(self.debug_draw)

        # Event loop
        while 1:

            t0 = time.time()
            self._handle_events()

            if self._exit:
                break

            self._surface.fill((0, 0, 0))
            self._step_world()
            pygame.display.update()

            t1 = time.time()

            delta = t1 - t0
            if delta < self._dt_s:
                time.sleep(self._dt_s - delta)

    def _zoom_in(self):
        self.debug_draw.scale *= 1.25

    def _zoom_out(self):
        self.debug_draw.scale *= 0.75

    def _handle_events(self):

        pressed_keys = pygame.key.get_pressed()
        pressed_mouse_buttons = pygame.mouse.get_pressed()

        # ctrl_pressed = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]

        drag_mode = pressed_mouse_buttons[0]

        if drag_mode and self._last_was_drag and self._handle_click:
            pos = pygame.mouse.get_pos()
            delta = [self._last_pos[0] - pos[0], self._last_pos[1] - pos[1]]
            translate = self.debug_draw.translate
            self.debug_draw.translate = (translate.x - delta[0], translate.y + delta[1])
        #
        self._last_was_drag = drag_mode
        self._last_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self._exit = True
                break

            # key events
            elif event.type == pygame.KEYDOWN:
                keycode = event.key
                name = pygame.key.name(event.key)
                self._testworld.on_keyboard_down(name)
            elif event.type == pygame.KEYUP:
                keycode = event.key
                name = pygame.key.name(event.key)
                self._testworld.on_keyboard_up(name)
            # mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    screen_pos = pos = pygame.mouse.get_pos()
                    world_pos = self.debug_draw.screen_to_world(screen_pos)
                    handled = self._testworld.on_mouse_down(world_pos)
                    self._handle_click = not handled

                # zoom
                if event.button == 4:
                    self._zoom_in()
                elif event.button == 5:
                    self._zoom_out()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    screen_pos = pos = pygame.mouse.get_pos()
                    world_pos = self.debug_draw.screen_to_world(screen_pos)
                    self._testworld.on_mouse_up(world_pos)
                self._handle_click = False

            elif event.type == pygame.MOUSEMOTION:
                screen_pos = pos = pygame.mouse.get_pos()
                world_pos = self.debug_draw.screen_to_world(screen_pos)
                self._testworld.on_mouse_move(world_pos)

    def _step_world(self):
        self._testworld.step(self._dt_s)
