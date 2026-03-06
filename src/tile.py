from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, Game, tile_position, tile_image, tile_type):
        super().__init__()
        self.game = Game
        self.position = tile_position
        self.tile_type = tile_type

    def update(self, offset:int=[0,0]):
        self.position[0] += offset[0]
        self.position[1] += offset[1]

    def  draw(self):
        self.game.camera.surface.blit()