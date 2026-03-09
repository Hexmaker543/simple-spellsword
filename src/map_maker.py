import pygame


class MapMaker:
    def __init__(self, Game, map_size:tuple[int,int]=(0,0), cell_size:float=16,
                     map_scale:int = 5):
        self.game = Game
        self.map_scale = map_scale
        self.map_size = map_size
        self.cell_size = cell_size * map_scale
        self.darkmode_on = False
        self.active_tile_index = 0
        self.tiles = self.game.map.tileset.non_empty_tiles
        self.grid = [[[] for _ in range(self.map_size[0])]
                                for _ in range(self.map_size[1])]
        self.grid_rects =  []

        self.toggle_darkmode()

    def pan(self, position_increment:list[int,int]):
        speed = self.cell_size
        if self.game.lshift_pressed: speed = speed * 5

        xstep = speed * position_increment[0]
        ystep = speed * position_increment[1]

        self.grid_rect.x += xstep
        self.grid_rect.y += ystep

        for row in self.grid_rects:
            for rect in row:
                rect.x += xstep
                rect.y += ystep

    def on_scroll(self, event):
        new_tile_index = self.active_tile_index + event.y
        
        if new_tile_index < 0: new_tile_index = len(self.tiles)-1
        if new_tile_index > len(self.tiles)-1: new_tile_index = 0

        self.active_tile_index = new_tile_index

    def on_click(self, event):
        mouse_position = pygame.mouse.get_pos()
        if not self.grid_rect.collidepoint(mouse_position): return

        left_click = event.button == 1
        right_click = event.button == 3

        if not left_click: return

        for y, row in enumerate (self.grid_rects):
            for x, rect in enumerate (row):
                if not rect.collidepoint(mouse_position): continue
                self._add_tile_to_map(x, y)

    def toggle_darkmode(self):
        if self.darkmode_on: 
            bg_checker_colors = (self.game.settings.WHITE,
                                 self.game.settings.GREY)
            grid_color = (0, 0, 0, 147)
            self.darkmode_on = False
        else:
            bg_checker_colors = (self.game.settings.BLACK,
                                self.game.settings.DARK_GREY)
            grid_color = (255, 255, 255, 147)
            self.darkmode_on = True

        self.grid_color = grid_color
        self.bg_checkerboard_colors = bg_checker_colors
        self._render_background()
        self._render_grid()

    def draw(self):
        self.game.screen.blit(self.bg_surface, self.bg_rect)
        self.game.screen.blit(self.grid_surface, self.grid_rect)
        self._draw_active_tile()

    def _draw_active_tile(self):
        mouse_position = pygame.mouse.get_pos()
        active_tile = self.tiles[self.active_tile_index][1]
        active_tile = pygame.transform.scale(active_tile, (self.cell_size, 
                                                           self.cell_size))
        active_tile_rect = active_tile.get_rect(bottomright = mouse_position)

        self.game.screen.blit(active_tile, active_tile_rect)

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
        self._render_tiles_on_map()
                
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
        pass

    def _add_tile_to_map(self, x, y):
        self.grid[y][x].append(self.active_tile_index)
        self._render_grid()
        