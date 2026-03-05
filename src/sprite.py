import pygame
from pygame.sprite import Sprite


class Sprite(Sprite):
    def __init__(self, Game, tile_position, tile_type):
        super().__init__()
        self.game = Game
        self.position = tile_position
        self.tile_type = tile_type

    def update(self, offset:int=0):
        pass