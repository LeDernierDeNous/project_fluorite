import pygame
import json
import os
from config import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from map.map_manager import MapManager
from biome.biome import Biome

# ==== Load Biomes from JSON ====
def load_biomes():
    try:
        with open('biomes.json', 'r') as f:
            biome_data = json.load(f)
            return [Biome(
                biome['name'],
                biome['height_min'],
                biome['height_max'],
                biome['humidity_min'],
                biome['humidity_max'],
                biome['temperature_min'],
                biome['temperature_max'],
                biome['mystical_min'],
                biome['mystical_max'],
                biome['resource_type'],
                biome['resource_variant'],
                tuple(biome['color'])  # Convert list to tuple for pygame color
            ) for biome in biome_data]
    except FileNotFoundError:
        print("ERROR: biomes.json not found!")
        return []
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON format in biomes.json!")
        return []
    except Exception as e:
        print(f"ERROR: Failed to load biomes: {str(e)}")
        return []

# ==== Setup ====
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Interactive 2D Biome Map")

# Load biomes from JSON
BIOMES = load_biomes()
if not BIOMES:
    print("No biomes loaded. Exiting...")
    pygame.quit()
    exit(1)

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
