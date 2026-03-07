import pygame
from tileset import Tileset
from tile import Tile
from pathlib import Path


class Map():
    def __init__(self, Game, map_file):
        super().__init__()
        self.game = Game
        self._import_map(map_file)

    def draw(self):
        self._draw_grid()

    def _draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, column in enumerate(row):
                for z, _ in enumerate(column):
                    self.grid[y][x][z].draw()

    def update(self):
        self.all_sprites.update()

    def _parse_words(self, line):
        normalized = " ".join(line.split())
        return [words.strip() for words in normalized.split(",")]
    
    def _handle_tileset(self, words):
        _, cell_size, padding, path = words
        padding = int(padding) or 0
        self.tileset = Tileset(self, path, int(cell_size), int(padding))

    def _handle_legend_entry(self, words):
        identifier = words[0]
        is_solid = bool(words[1])
        image_x = int(words[2])
        image_y = int(words[3])
        image = self.tileset.get_tile(image_x, image_y)
        self.legend[identifier] = [is_solid, image]

    def _create_tile(self, identifier, x, y):
        is_solid = self.legend[identifier][0]
        image = self.legend[identifier][1]
        return Tile(Game=self.game, 
            tile_position=[x,y], 
            tile_identifier=identifier,
            image=image,
            is_solid=is_solid,
        )
    
    def _add_tile(self, identifier, x, y):
        new_tile = self._create_tile(identifier, x, y)
        self.grid[y][x].append(new_tile)
        self.all_sprites.add(new_tile)

    def _handle_sprite_entry(self, line, y):
        identifiers = self.legend.keys()
        reading_stacked_tile = False
        char_cache = ''
        x = 0
        for char in line:
            char_cache += char
            if reading_stacked_tile and char == ']':
                x += 1 
                reading_stacked_tile = False

            elif char == '[': reading_stacked_tile = True     
            
            elif char_cache in identifiers:
                self._add_tile(char_cache, x, y)
                if not reading_stacked_tile: x += 1
            
            else: continue

            char_cache = ''

    def _import_map(self, map_file):
        mapfile = Path(map_file)
        mapdata = mapfile.read_text()

        self.legend = {}
        reading_map = False
        line_number = 0
        for raw_line in mapdata.splitlines():
            if '--' in raw_line: continue
            
            elif 'START_MAP' in raw_line:
                reading_map = True

            elif 'END_MAP' in raw_line:
                reading_map = False

            elif not reading_map:
                words = self._parse_words(raw_line)
                if not words or not words[0]:
                    continue
                
                elif words[0] == 'MAP_SIZE': 
                    x = 1
                    y = 2
                    self.map_size = int(words[x]), int(words[y])

                elif words[0] == 'TILEMAP_PATH':
                    self._handle_tileset(words)
                
                else:
                    self._handle_legend_entry(words)
            
            elif reading_map:
                self.all_sprites = pygame.sprite.Group()
                self.grid = [[[] for _ in range(self.map_size[0])] 
                                 for _ in range(self.map_size[1])]
                self._handle_sprite_entry(raw_line, line_number)
                line_number += 1

            else: raise NotImplemented(
                f"Error. Cannot parse line {line_number+1} in '{map_file}'"
                )