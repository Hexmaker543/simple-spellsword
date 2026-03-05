import pygame
from tileset import Tileset
from tile_type import TileType
from sprite import Sprite
from pathlib import Path


class Map():
    def __init__(self, Game):
        super().__init__()
        self.game = Game

        self.sprites = pygame.sprite.Group()

    def _parse_words(self, line):
        normalized = " ".join(line.split())
        return [w.strip() for w in normalized.split(",")]
    
    def _handle_tileset(self, words):
        _, path, cell_size, padding = words
        padding = padding or 0
        self.tileset = Tileset(self, path, cell_size, padding)

    def _handle_legend_entry(self, words):
        identifier, name, solid, image = words
        self.legend[identifier] = TileType(name, identifier, image, solid)

    def _handle_sprite_entry(self, line):
        delimiters = {
            'tile stackers' : ['[', ']', '(', ')'],
            'separators' : [',','.','-','_']
            }
        identifiers = self.legend.keys()
        for char in line:
            if char not in identifiers or delimiters: continue
            if char in delimiters['separators']: continue

            if char in identifiers: pass

    def _import_map(self, map_file):
        mapfile = Path("assets/map.map")
        mapdata = mapfile.read_text()

        self.legend = {}
        reading_map = False
        for raw_line in mapdata.splitlines():
            if '--' in raw_line: continue
            if 'START_MAP' in raw_line:
                reading_map = True
                continue

            if 'END_MAP' in raw_line:
                reading_map = False
                continue

            if not reading_map:
                words = self._parse_words(raw_line)

                if not words or not words[0]:
                    continue

                if words[0] == 'TILEMAP_PATH':
                    self._handle_tileset(words)
                else:
                    self._handle_legend_entry(words)
            else: self._handle_sprite_entry(raw_line)
                

    def _create_sprite(self, tile_position, Sprite):
        self.sprites[tile_position[0]][tile_position[1]] = Sprite