import pygame, sys
from settings import Settings
from camera import Camera


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self._initialize_screen()

        self.camera = Camera(self, (0,0,self.screen.get_width(), 
                                    self.screen.get_height()))

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

    def get_pixel_position(self, tile_position):
        tile_size = self.settings.BASE_TILE_SIZE
        x_position = tile_position[0] * tile_size
        y_position = tile_position[1] * tile_size
        pixel_position = [x_position, y_position]

        return pixel_position


game = Game()
game.run()