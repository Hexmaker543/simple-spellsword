import pygame
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, Game, tile_position, image, tile_identifier, is_solid:bool=False):
        super().__init__()
        self.game = Game
        self.position = tile_position
        self.image = image
        self.identifier = tile_identifier
        self.is_solid = is_solid

        self._render()
        self.update()

    def update(self, offset:int=[0,0]):
        self.position[0] += offset[0]
        self.position[1] += offset[1]
        self.game.convert_position_to_pixel_position(self)

    def draw(self):
        self.game.camera.surface.blit(self.surface, self.rect)

    def _render(self):
        self.surface = self.image
        self.rect = self.surface.get_rect()