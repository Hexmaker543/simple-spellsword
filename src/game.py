import pygame, sys
from settings import Settings
from camera import Camera
from map import Map
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self._initialize_screen()

        self.camera = Camera(self, (0,0, self.screen.get_width(), 
                                    self.screen.get_height()))
        self.map = Map(self, self.settings.map)
        self.player = Player(self, [5,10], [0,0])
        self.camera.set_focus(self.player)

    def _initialize_screen(self):
        self.screen = pygame.display.set_mode(self.settings.BASE_WINDOW_SIZE)
        self.rect = self.screen.get_rect()

    def run(self):
        while True:
            self._update()
            self._draw()
            self._handle_input()
            pygame.display.flip()

    def _update(self):
        self.camera.update()

    def _draw(self):
        self.screen.fill(self.settings.BASE_WINDOW_BACKGROUND_COLOR)
        self.camera.surface.fill(self.settings.BASE_WINDOW_BACKGROUND_COLOR)
        self.camera.draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN: self._handle_keydown_events(event)

    def _handle_keydown_events(self, event):
        if event.key == pygame.K_w: self.player.move([0,-1])
        if event.key == pygame.K_s: self.player.move([0,1])
        if event.key == pygame.K_d: self.player.move([1,0])
        if event.key == pygame.K_a: self.player.move([-1,0])

    def convert_position_to_pixel_position(self, object, offset:list[int,int]=(0,0)):
        tile_size = self.map.cell_size
        pos_x = (object.position[0] + offset[0]) * tile_size
        pos_y = (object.position[1] + offset[1]) * tile_size

        object.rect.topleft = (pos_x, pos_y)


game = Game()
game.run()