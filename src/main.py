import pygame
from config import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from map.map_manager import MapManager
from biome.biome import Biome

# ==== Biomes List ====
BIOMES = [
    Biome("Whispering Grove", (34, 139, 34), (0.2, 0.6), (0.7, 1.0), (0.4, 0.8), (0.5, 0.6), "wood", "Whisperwood Timber"),
    Biome("Scorched Desert", (210, 180, 140), (0.0, 0.3), (0.0, 0.4), (0.7, 1.0), (0.0, 0.2), "stone", "Desert Marble"),
    Biome("Mystic Peaks", (160, 82, 45), (0.7, 1.0), (0.3, 0.7), (0.2, 0.6), (0.7, 1.0), "ore", "Magic Infused Ore"),
    # Add more biomes here
]

# ==== Setup ====
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Interactive 2D Biome Map")

map_manager = MapManager(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, BIOMES)

# ==== Main Loop ====
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            tile = map_manager.get_tile_at_pixel(mx, my)
            if tile:
                print(f"Clicked Tile ({tile.x}, {tile.y}): {tile.biome.name} ({tile.biome.resource_type} - {tile.biome.resource_variant})")

    screen.fill((0, 0, 0))
    map_manager.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
