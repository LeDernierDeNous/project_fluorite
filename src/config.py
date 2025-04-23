# Basic configuration

class Config:
    def __init__(self):
        self.MAP_WIDTH = 20
        self.MAP_HEIGHT = 20
        self.TILE_SIZE = 32
        self.WINDOW_WIDTH = self.MAP_WIDTH * self.TILE_SIZE
        self.WINDOW_HEIGHT = self.MAP_HEIGHT * self.TILE_SIZE

    def get_map_dimensions(self):
        return self.MAP_WIDTH, self.MAP_HEIGHT

    def get_window_dimensions(self):
        return self.WINDOW_WIDTH, self.WINDOW_HEIGHT

    def get_tile_size(self):
        return self.TILE_SIZE
