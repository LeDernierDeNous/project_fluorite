# Basic configuration
from ui.style import ColorPalette

class Config:
    def __init__(self):
        # Map configuration
        self.MAP_WIDTH = 200
        self.MAP_HEIGHT = 100
        self.TILE_SIZE = 16
        
        # Window configuration
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        # UI configuration
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.MENU_BACKGROUND_COLOR = (50, 50, 50)
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER_COLOR = (150, 150, 150)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        
        # Theme configuration
        self.DEFAULT_THEME = ColorPalette.DARK

    def get_map_dimensions(self):
        return self.MAP_WIDTH, self.MAP_HEIGHT

    def get_window_dimensions(self):
        return self.WINDOW_WIDTH, self.WINDOW_HEIGHT

    def get_tile_size(self):
        return self.TILE_SIZE
