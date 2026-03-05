import pygame, sys
from settings import Settings
from camera import Camera
from tileset import Tileset
from tile_type import TileType


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self._initialize_screen()

    def _initialize_screen(self):
        self.screen = pygame.display.set_mode(self.settings.BASE_WINDOW_SIZE)
        self.rect = self.screen.get_rect()

    def run(self):
        while True:
            self._handle_input()
            self.screen.fill(self.settings.BASE_WINDOW_BACKGROUND_COLOR)
            pygame.display.flip()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


game = Game()
game.run()