import pygame, sys
from settings import Settings
from map import Map
from map_maker import MapMaker
from player import Player


class Game:
    def __init__(self):
        # Flags
        self.map_maker_active = False
        self.lctrl_pressed = False
        self.lshift_pressed = False

        pygame.init()
        self.settings = Settings()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self._initialize_screen()
        pygame.mouse.set_visible(False)

        self.map = Map(self, self.settings.map)
        self.map_maker = MapMaker(self, (15,15), 12)
        self.player = Player(self, [5,10], [0,0])

    def _initialize_screen(self):
        self.screen = pygame.display.set_mode(self.settings.BASE_WINDOW_SIZE)
        self.rect = self.screen.get_rect()

    def run(self):
        while True:
            self.clock.tick(self.settings.FRAMERATE)
            self._update()
            self._draw()
            self._handle_input()
            pygame.display.flip()

    def _update(self):
        if self.map_maker_active: self.map_maker.update()
        else: self.map.update()

    def _draw(self):
        self.screen.fill(self.settings.BASE_WINDOW_BACKGROUND_COLOR)
        if self.map_maker_active: self.map_maker.draw()
        else: self.map.draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN: self._handle_keydown_events(event)
            if event.type == pygame.KEYUP: self._handle_keyup_events(event)
            if event.type == pygame.MOUSEWHEEL: 
                if self.map_maker_active: self.map_maker.on_scroll(event)
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if self.map_maker_active: self.map_maker.on_click(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.map_maker_active: self.map_maker.off_click(event)

    def _handle_keydown_events(self, event):
        m_pressed = pygame.key.get_pressed()[pygame.K_m]

        if event.key == pygame.K_LSHIFT: self.lshift_pressed = True
        if event.key == pygame.K_LCTRL: self.lctrl_pressed = True

        if self.lshift_pressed and self.lctrl_pressed and m_pressed:
            if not self.settings.MAP_MAKER_ON: return
            if self.map_maker_active: self.map_maker_active = False
            else: self.map_maker_active = True

        if event.key == pygame.K_ESCAPE: sys.exit()

        self._handle_player_controls(event)
        self._handle_map_maker_controls(event)

    def _handle_player_controls(self, event):
        if self.map_maker_active: return
        if event.key == pygame.K_w: self.player.move((0,-1))
        if event.key == pygame.K_s: self.player.move((0,1))
        if event.key == pygame.K_d: self.player.move((1,0))
        if event.key == pygame.K_a: self.player.move((-1,0))

    def _handle_map_maker_controls(self, event):
        if not self.map_maker_active: return
        if event.key == pygame.K_w: self.map_maker.pan((0,1))
        if event.key == pygame.K_s: self.map_maker.pan((0,-1))
        if event.key == pygame.K_d: self.map_maker.pan((-1,0))
        if event.key == pygame.K_a: self.map_maker.pan((1,0))

        if event.key == pygame.K_TAB: self.map_maker.toggle_darkmode()

        if event.key == pygame.K_e: self.map_maker.save_map()

    def _handle_keyup_events(self, event):
        if event.key == pygame.K_LSHIFT: self.lshift_pressed = False
        if event.key == pygame.K_LCTRL: self.lctrl_pressed = False

    def convert_position_to_pixel_position(self, object):
        tile_size = self.map.cell_size
        pos_x = object.position[0] * tile_size
        pos_y = object.position[1] * tile_size

        object.rect.topleft = (pos_x, pos_y)


game = Game()
game.run()