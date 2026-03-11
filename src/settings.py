class Settings:
    def __init__(self):
        self.FRAMERATE = 120

        # Assets
        self.spritemap = r"C:\Users\asmod\Lair\Projects\Simple SpellSword\assets\UnizenCustom.png"
        self.map = r"C:\Users\asmod\Lair\Projects\Simple SpellSword\assets\test.map"

        # Color
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.GREY = (147,147,147)
        self.DARK_GREY = (100,100,100)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)

        # Screen
        self.WINDOW_TITLE = "Simple Spellsword"
        self.BASE_WINDOW_SIZE = (896, 896)
        self.BASE_WINDOW_BACKGROUND_COLOR = self.BLACK

        # Map
        self.BASE_TILE_SIZE = 12

        # Map Maker 
        self.MAP_MAKER_ON = True