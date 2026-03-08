import pygame


class Player:
    def __init__(self, Game, position:list[int,int]=[0,0], 
                 sprite:list[int,int]=[0,0]):
        self.game = Game
        self.sprite = sprite
        self.position = position
        self.render()
        self.move()

    def move(self, position_increment:tuple[int,int]=(0,0)):
        new_position_x = position_increment[0] + self.position[0]
        new_position_y = position_increment[1] + self.position[1]
        new_position = [new_position_x, new_position_y]
        if self._can_move(new_position):
            self.position = new_position
        self.game.convert_position_to_pixel_position(self)

    def draw(self):
        self.game.map.surface.blit(self.surface, self.rect)

    def render(self):
        self.surface = self.game.map.tileset.tiles[self.sprite[0]][self.sprite[1]]
        self.rect = self.surface.get_rect()

    def _can_move(self, tile:tuple[int,int]):
        for layer in self.game.map.grid[tile[1]][tile[0]]:
            if layer.is_solid: return False
        else: return True