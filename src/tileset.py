import pygame


class Tileset:
    def __init__(self, Game, tileset_filepath, cell_size, padding:int=0):
        self.game = Game
        self.filepath = tileset_filepath
        self.cell_size = cell_size
        self.padding = padding
        self._render_tileset()
        self._get_tiles()

    def _render_tileset(self):
        self.surface = pygame.image.load(self.filepath).convert_alpha()

    def _get_tiles(self):
        self.tiles = []
        step_value = self.cell_size + self.padding
        image_width = self.surface.get_width()
        image_height = self.surface.get_height() 
        for y in range(0, image_height, step_value):
            new_row = []
            for x in range(0, image_width, step_value):
                new_tile = self.surface.subsurface(x+self.padding, 
                                                   y+self.padding, 
                                                   self.cell_size,
                                                   self.cell_size)
                new_row.append(new_tile)
            self.tiles.append(new_row)

    def get_tile(self, tile_column, tile_row):
        return self.tiles[tile_column][tile_row]