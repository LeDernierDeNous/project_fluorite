import pygame
from config import Config
from map.map_manager import MapManager
from biome.biome_loader import BiomeLoader

class Game:
    def __init__(self):
        self.config = Config()
        self.screen = None
        self.clock = None
        self.map_manager = None
        self.running = False

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.config.get_window_dimensions())
        pygame.display.set_caption("Interactive 2D Biome Map")
        self.clock = pygame.time.Clock()

        # Load biomes and create map
        biome_loader = BiomeLoader()
        biomes = biome_loader.load()
        if not biomes:
            print("No biomes loaded. Exiting...")
            pygame.quit()
            exit(1)

        map_width, map_height = self.config.get_map_dimensions()
        self.map_manager = MapManager(map_width, map_height, self.config.get_tile_size(), biomes)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        mx, my = pos
        tile = self.map_manager.get_tile_at_pixel(mx, my)
        if tile:
            print(f"Clicked Tile ({tile.x}, {tile.y}): {tile.biome.name} ({tile.biome.resource_type} - {tile.biome.resource_variant})")

    def update(self):
        pass  # Add game logic updates here

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map_manager.render(self.screen)
        pygame.display.flip()

    def run(self):
        self.initialize()
        self.running = True

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit() 