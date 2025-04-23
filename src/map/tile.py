from biome.biome import generate_properties

class Tile:
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome
        self.properties = self.biome.generate_properties()

    def render(self, screen, tile_size):
        import pygame
        rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self.biome.color, rect)
