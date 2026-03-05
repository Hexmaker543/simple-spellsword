import pygame


class Player:
    def __init__(self, Game, position:list[int,int]=[0,0]):
        self.game = Game
        self.position = position
        self.render()

    def move(self, position_increment):
        new_position = position_increment + self.position
        if self._can_move(new_position): self.position = new_position

    def draw(self):
        self.game.camera.blit(self.surface, self.rect)

    def render(self):
        self.surface = pygame.image.load(
            self.game.settings.tilemmap
            ).convert_alpha()
        self.rect = self.surface.get_rect(
            topleft = self.game.get_pixel_position(self.position)
            )

    def _can_move(self, tile:tuple[int,int]):
        if self.game.tiles[tile[0]][tile[1]].is_solid: return False
        else: return True