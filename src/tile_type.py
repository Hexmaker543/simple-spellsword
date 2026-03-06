class TileType:
    def __init__(self, name, 
                 tile_identifier, 
                 is_solid:bool=False):
        self.name = name
        self.tile_identifier = tile_identifier
        self.is_solid = is_solid
