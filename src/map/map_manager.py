import random
from map.tile import Tile
import noise

class MapManager:
    def __init__(self, width, height, tile_size, biomes):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.biomes = biomes
        self.tiles = []

        self.generate_map()

    def generate_map(self):
        scale = 50.0

        for y in range(self.height):
            row = []
            for x in range(self.width):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5

                height_val = noise.pnoise2(nx * scale, ny * scale, octaves=4, repeatx=1024, repeaty=1024, base=0)
                humidity_val = noise.pnoise2(nx * scale, ny * scale, octaves=4, repeatx=1024, repeaty=1024, base=1)
                temperature_val = noise.pnoise2(nx * scale, ny * scale, octaves=4, repeatx=1024, repeaty=1024, base=2)
                mystical_val = noise.pnoise2(nx * scale, ny * scale, octaves=4, repeatx=1024, repeaty=1024, base=3)

                height_val = (height_val + 0.5)
                humidity_val = (humidity_val + 0.5)
                temperature_val = (temperature_val + 0.5)
                mystical_val = (mystical_val + 0.5)

                selected_biome = random.choice(self.biomes)  # fallback biome
                for biome in self.biomes:
                    if biome.matches(height_val, humidity_val, temperature_val, mystical_val):
                        selected_biome = biome
                        break

                row.append(Tile(x, y, selected_biome))
            self.tiles.append(row)

    def render(self, surface):
        for row in self.tiles:
            for tile in row:
                rect = (
                    tile.x * self.tile_size,
                    tile.y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                surface.fill(tile.biome.color, rect)

    def get_tile_at_pixel(self, px, py):
        tx = px // self.tile_size
        ty = py // self.tile_size

        if 0 <= tx < self.width and 0 <= ty < self.height:
            return self.tiles[ty][tx]
        return None
