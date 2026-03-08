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

    def update(self, offset:int=[0,0]):
        self.game.convert_position_to_pixel_position(self, offset)

    def draw(self):
        self.game.map.surface.blit(self.surface, self.rect)

    def _render(self):
        self.surface = self.image
        self.rect = self.surface.get_rect()