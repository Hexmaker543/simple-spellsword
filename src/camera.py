import pygame


class Camera:
    def __init__(self, Game, camera_rect):
        self.game = Game
        self.focus_object = None
        if camera_rect: self.set_rect(camera_rect)
        else: self.set_rect(0,0,0,0)

    def draw(self):
        self.game.map.draw()
        self.game.screen.blit(self.surface, self.rect)

    def update(self):
        new_offset_x = 0
        new_offset_y = 0
        if self.focus_object.position[0] != self.last_focus_object_position[0]:
            new_offset_x = (
                self.last_focus_object_position[0] - 
                self.focus_object.position[0]
                )
        if self.focus_object.position[1] != self.last_focus_object_position[1]:
            new_offset_y = (
                self.last_focus_object_position[1] - 
                self.focus_object.position[1] 
                )
        
        self.sprite_offset[0] += new_offset_x
        self.sprite_offset[1] += new_offset_y

        self.game.map.all_sprites.update(self.sprite_offset)
        self.last_focus_object_position = self.focus_object.position

    def set_rect(self, rect):
        if isinstance(rect, pygame.Rect):
            self.rect = rect
        else:
            self.rect = pygame.Rect(rect)

        self.surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
            )

    def set_focus(self, focus_object):
        self.focus_object = focus_object
        self.base_focus_object_position = self.focus_object.position
        self.last_focus_object_position = self.focus_object.position
        self.sprite_offset = [0,0]