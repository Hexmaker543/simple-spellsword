class TileType:
    def __init__(self, Game, name, 
                 tile_variable, 
                 tile_image, 
                 is_solid:bool=False):
        self.game = Game
        self.name = name
        tile_variable
        self.is_solid = is_solid
        self.tile_image = tile_image
