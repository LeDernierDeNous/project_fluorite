# Basic configuration

class Config:
    def __init__(self):
        # Map configuration
        self.MAP_WIDTH = 100
        self.MAP_HEIGHT = 50
        self.TILE_SIZE = 16
        self.WINDOW_WIDTH = self.MAP_WIDTH * self.TILE_SIZE
        self.WINDOW_HEIGHT = self.MAP_HEIGHT * self.TILE_SIZE

        # UI configuration
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.MENU_BACKGROUND_COLOR = (50, 50, 50)
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER_COLOR = (150, 150, 150)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)

    def get_map_dimensions(self):
        return self.MAP_WIDTH, self.MAP_HEIGHT

    def get_window_dimensions(self):
        return self.WINDOW_WIDTH, self.WINDOW_HEIGHT

    def get_tile_size(self):
        return self.TILE_SIZE
