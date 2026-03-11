import pygame
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


class MapMaker:
    def __init__(self, Game, map_size:tuple[int,int]=(0,0), cell_size:float=16,
                     map_scale:int = 5):
        self.game = Game
        self.map_scale = map_scale
        self.map_size = map_size
        self.cell_size = cell_size * map_scale
        self.darkmode_on = True
        self.left_mouse_button_pressed = False
        self.right_mouse_button_pressed = False
        self.previously_removed_tile = None
        self.previously_added_tile = None
        self.previous_active_tile_index = None
        self.active_tile_index = 0
        self.tiles = self.game.map.tileset.non_empty_tiles
        self.grid = [[[] for _ in range(self.map_size[0])]
                                for _ in range(self.map_size[1])]
        self.grid_rects =  []
        self.scroll_offset = [0,0]

        self.toggle_darkmode()
        self._render_map()

    def pan(self, position_increment:list[int,int]):
        speed = self.cell_size
        if self.game.lshift_pressed: speed = speed * 5

        xstep = speed * position_increment[0]
        ystep = speed * position_increment[1]

        self.grid_rect.x += xstep
        self.grid_rect.y += ystep

    def on_scroll(self, event):
        new_tile_index = self.active_tile_index + event.y
        
        if new_tile_index < 0: new_tile_index = len(self.tiles)-1
        if new_tile_index > len(self.tiles)-1: new_tile_index = 0

        self.active_tile_index = new_tile_index

    def on_click(self, event):
        left_click = event.button == 1
        right_click = event.button == 3 
        
        if left_click: self.left_mouse_button_pressed = True
        if right_click: self.right_mouse_button_pressed = True

    def off_click(self, event):
        left_click = event.button == 1
        right_click = event.button == 3 
        
        if left_click: self.left_mouse_button_pressed = False
        if right_click: 
            self.right_mouse_button_pressed = False
            self.previously_removed_tile = None

    def _get_clicked_tile(self):
        mouse_position = pygame.mouse.get_pos()

        local_x = mouse_position[0] - self.grid_rect.x
        local_y = mouse_position[1] - self.grid_rect.y
        local_mouse_pos = (local_x, local_y)

        for y, row in enumerate(self.grid_rects):
            for x, rect in enumerate(row):
                if rect.collidepoint(local_mouse_pos):
                    return x, y
            
    def toggle_darkmode(self):
        if self.darkmode_on: 
            bg_checker_colors = (self.game.settings.WHITE,
                                 self.game.settings.GREY)
            grid_color = (255, 255, 255, 147)
            self.darkmode_on = False
        else:
            bg_checker_colors = (self.game.settings.BLACK,
                                self.game.settings.DARK_GREY)
            grid_color = (0, 0, 0, 147)
            self.darkmode_on = True

        self.grid_color = grid_color
        self.bg_checkerboard_colors = bg_checker_colors
        self._render_background()
        self._render_grid()

    def draw(self):
        self.game.screen.blit(self.bg_surface, self.bg_rect)
        self.game.screen.blit(self.map_surface, self.grid_rect)
        self.game.screen.blit(self.grid_surface, self.grid_rect)
        self._draw_active_tile()

    def _draw_active_tile(self):
        mouse_position = pygame.mouse.get_pos()
        active_tile = self.tiles[self.active_tile_index][1]
        active_tile = pygame.transform.scale(active_tile, (self.cell_size, 
                                                           self.cell_size))
        active_tile_rect = active_tile.get_rect(center = mouse_position)

        self.game.screen.blit(active_tile, active_tile_rect)

    def _render_map(self):
        width = self.grid_surface.get_width()
        height = self.grid_surface.get_height()

        self.map_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.map_rect = self.map_surface.get_rect()

        for y, row in enumerate(self.grid):
            for x, layer in enumerate(row):
                for tile_index in layer:
                    tile_image = self.tiles[tile_index][1]
                    tile_image = pygame.transform.scale_by(tile_image,
                                                           self.map_scale)
                    self.map_surface.blit(tile_image, self.grid_rects[y][x])

    def _render_grid(self):
        width = self.map_size[0] * self.cell_size
        height = self.map_size[1] * self.cell_size

        self.grid_surface = pygame.Surface((width+1, height+1), pygame.SRCALPHA)
        has_drawn_x_lines = False
        for y in range(0, height+1, self.cell_size):
            new_row = []
            pygame.draw.line(self.grid_surface, self.grid_color, 
                             (0, y), 
                             (width, y))
            for x in range(0, width+1, self.cell_size):
                new_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                new_row.append(new_rect)

                if has_drawn_x_lines: continue
                pygame.draw.line(self.grid_surface, self.grid_color, 
                             (x, 0), 
                             (x, height))
            self.grid_rects.append(new_row)
            has_drawn_x_lines = True
                
        self.grid_rect = self.grid_surface.get_rect(
            center = self.game.rect.center)
        
    def _render_tiles_on_map(self):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                for tile_index in tile:
                    self.grid_surface.blit(self.tiles[tile_index][1], 
                                           self.grid_rects[y][x])

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
        self._update_mouse_on_map_bool()
        self._refresh_active_tile_cache_on_index_switch()

        self._remove_tile_from_map()
        self._add_tile_to_map()

    def _update_mouse_on_map_bool(self):
        mouse_position = pygame.mouse.get_pos()
        
        if self.grid_rect.collidepoint(mouse_position):
            self.mouse_on_map = True
        else: self.mouse_on_map = False

    def _refresh_active_tile_cache_on_index_switch(self):
        if self.previous_active_tile_index == self.active_tile_index: return
        else:
            self.previously_added_tile = None
            self.previously_removed_tile = None
            self.previous_active_tile_index = self.active_tile_index

    def _add_tile_to_map(self):
        if not self.left_mouse_button_pressed: return
        if not self.mouse_on_map: return

        x, y = self._get_clicked_tile()
        try: 
            if self.grid[y][x]: pass
        except IndexError: return
        if self.previously_added_tile == [x,y]: return

        if self.active_tile_index in self.grid[y][x]: return
        self.grid[y][x].append(self.active_tile_index)

        self.previously_added_tile = [x,y]
        self._render_map()

    def _remove_tile_from_map(self):
        if self.left_mouse_button_pressed: return
        if not self.right_mouse_button_pressed: return
        if not self.mouse_on_map: return
        
        x, y = self._get_clicked_tile()
        try: 
            if self.grid[y][x]: pass
        except IndexError: return
        if self.previously_removed_tile == [x,y]: return

        try: self.grid[y][x].pop()
        except IndexError: pass
        
        if self.game.lshift_pressed: self.grid[y][x] = []
        
        self.previously_removed_tile = [x,y]
        self._render_map()

    def save_map(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        save_file = filedialog.asksaveasfile(mode="w", defaultextension='.map',
                                             title="Save map")
        
        map_sizex = self.map_size[0]
        map_sizey = self.map_size[1]
        map_scale = self.game.map.tile_scale
        padding = self.game.map.tileset.padding
        cell_size = self.cell_size
        tileset_filepath = self.game.map.tileset.filepath

        save_file.write(
f"""MAP_SIZE, {map_sizex}, {map_sizey}, {map_scale}

TILEMAP_PATH, {cell_size}, {padding}, {tileset_filepath}

""")
        printed_layers = []
        for row in self.grid:
            for tile in row:
                for layer in tile:
                    if layer in printed_layers: continue
                    
                    tilex = self.tiles[layer][0][0]
                    tiley = self.tiles[layer][0][1]
                    
                    save_file.write(f"{layer}, false, {tilex}, {tiley}\n")
                    
                    printed_layers.append(layer)

        save_file.write('\nSTART_MAP\n')
        for row in self.grid:
            for tile in row:
                save_file.write(str(tile))
            save_file.write('\n')
        save_file.write('END_MAP')

        root.destroy()