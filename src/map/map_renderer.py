import pygame
from config import TILE_SIZE
from biome.biome_colors import BIOME_COLORS

class MapRenderer:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.map = game_map

    def draw(self):
        for y, row in enumerate(self.map.tiles):
            for x, tile in enumerate(row):
                color = BIOME_COLORS.get(tile.biome.name, (0, 0, 0))  # default to black
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
