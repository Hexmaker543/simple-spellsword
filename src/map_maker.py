import pygame
import tkinter as tk
from tkinter import filedialog

class MapMaker:
    def __init__(self, Game, map_size:tuple[int,int]=(0,0), cell_size:float=16,
                     map_scale:int = 5):
        self.game = Game
        self.map_scale = map_scale
        self.map_size = map_size
        self.cell_size = cell_size * map_scale
        self.grid_color = (0, 0, 0, 147)
        self.bg_checkerboard_colors = (self.game.settings.WHITE,
                                       self.game.settings.GREY)
        
        self._render_background()
        self._render_grid()

    def draw(self):
        self.game.screen.blit(self.bg_surface, self.bg_rect)
        self.game.screen.blit(self.grid_surface, self.grid_rect)

    def _render_grid(self):
        width = self.map_size[0] * self.cell_size
        height = self.map_size[1] * self.cell_size

        self.grid_surface = pygame.Surface((width+1, height+1), pygame.SRCALPHA)

        for y in range(0, height+1, self.cell_size):
            pygame.draw.line(self.grid_surface, self.grid_color, 
                             (0, y), 
                             (width, y))
            for x in range(0, width+1, self.cell_size):
                pygame.draw.line(self.grid_surface, self.grid_color, 
                             (x, 0), 
                             (x, height))
                
        self.grid_rect = self.grid_surface.get_rect()

    def _render_background(self):
        checkers_per_screen = 5
        width = self.game.screen.get_width()
        height = self.game.screen.get_width()
        square_size = width//checkers_per_screen

        self.bg_surface = pygame.Surface((width, height))
        self.bg_rect = self.bg_surface.get_rect()
        
        color1 = self.bg_checkerboard_colors[0]
        color2 = self.bg_checkerboard_colors[1]
        is_color1 = False
        step_value = square_size
        for y in range(0, height, step_value):
            if is_color1: is_color1 = False
            else: is_color1 = True
            for x in range(0, width, step_value):
                if is_color1: 
                    color = color1
                    is_color1 = False 
                else: 
                    color = color2
                    is_color1 = True
                
                pygame.draw.rect(self.bg_surface, color, (x, y, 
                                                          square_size, 
                                                          square_size))
            self.bg_surface = pygame.transform.box_blur(self.bg_surface, 5)

    def update(self):
        pass