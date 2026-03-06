import pygame
from tileset import Tileset
from tile_type import TileType
from tile import Tile
from pathlib import Path


class Map():
    def __init__(self, Game, map_file):
        super().__init__()
        self.game = Game
        self._import_map(map_file)

    def _parse_words(self, line):
        normalized = " ".join(line.split())
        return [words.strip() for words in normalized.split(",")]
    
    def _handle_tileset(self, words):
        _, path, cell_size, padding = words
        padding = padding or 0
        self.tileset = Tileset(self, path, cell_size, padding)

    def _handle_legend_entry(self, words):
        identifier, name, solid, image = words
        self.legend[identifier] = TileType(name, identifier, image, solid)

    def _handle_sprite_entry(self, line, y):
        identifiers = self.legend.keys()
        reading_stacked_tile = False
        char_cache = ''
        x = 0

        for char in line:
            char_cache += char

            if reading_stacked_tile:
                char_cache += char
                if char == ']':
                    x += 1 
                    reading_stacked_tile = False
                
                elif char_cache in identifiers:
                    new_tile = Tile(self, [x,y], self.legend[char_cache])
                    self.grid.append(new_tile)
                    self.all_sprites.add(new_tile)

            elif char == '[': reading_stacked_tile = True     
            elif char_cache in identifiers:
                self.grid.append(new_tile)
                self.all_sprites.add(Tile(self, [x,y], self.legend[char_cache]))
                x += 1
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
                if words[0] == 'MAP_SIZE': 
                    map_size = 1
                    self.map_size = words[map_size]
                if words[0] == 'TILEMAP_PATH':
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

    def _create_sprite(self, tile_position, Sprite):
        self.sprites[tile_position[0]][tile_position[1]] = Sprite