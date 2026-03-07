class Settings:
    def __init__(self):
        # Assets
        self.spritemap = r"C:\Users\asmod\Lair\Projects\Simple SpellSword\assets\UnizenCustom.png"
        self.map = r"C:\Users\asmod\Lair\Projects\Simple SpellSword\assets\map.map"

        # Color
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)

        # Screen
        self.WINDOW_TITLE = "Simple Spellsword"
        self.BASE_WINDOW_SIZE = (896, 896)
        self.BASE_WINDOW_BACKGROUND_COLOR = self.BLACK

        # Map
        self.BASE_TILE_SIZE = 12