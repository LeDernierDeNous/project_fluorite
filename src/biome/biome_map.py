import pygame
from typing import List, Tuple, Optional
from .biome import Biome
from noise_layer import NoiseLayer

class BiomeMap:
    def __init__(self, biomes: List[Biome]):
        self.biomes = biomes
        self.cell_size = 20
        self.grid_width = 40
        self.grid_height = 30
        self.screen_width = 800
        self.screen_height = 600
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Tooltip properties
        self.hovered_tile: Optional[Tuple[int, int]] = None
        self.font = pygame.font.Font(None, 24)
        
        # Generate all noise maps with different scales for variety
        self.height_map = NoiseLayer(self.grid_width, self.grid_height, scale=20.0)
        self.humidity_map = NoiseLayer(self.grid_width, self.grid_height, scale=15.0)
        self.temperature_map = NoiseLayer(self.grid_width, self.grid_height, scale=25.0)
        self.mystical_map = NoiseLayer(self.grid_width, self.grid_height, scale=30.0)
        
        # Create a 2D grid to store biome information
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self._generate_biome_grid()
        self._center_map()

    def update_screen_size(self, width: int, height: int):
        """Update screen dimensions and recenter the map"""
        self.screen_width = width
        self.screen_height = height
        self._center_map()

    def _center_map(self):
        """Center the map in the current window"""
        total_width = self.grid_width * self.cell_size
        total_height = self.grid_height * self.cell_size
        self.offset_x = (self.screen_width - total_width) // 2
        self.offset_y = (self.screen_height - total_height) // 2

    def _generate_biome_grid(self):
        # Generate properties for each grid cell using noise maps
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Get all values from noise maps
                height = self.height_map.get(x, y)
                humidity = self.humidity_map.get(x, y)
                temperature = self.temperature_map.get(x, y)
                mystical = self.mystical_map.get(x, y)
                
                # Find matching biome based on all properties
                for biome in self.biomes:
                    if (biome.height_min <= height <= biome.height_max and 
                        biome.humidity_min <= humidity <= biome.humidity_max and
                        biome.temperature_min <= temperature <= biome.temperature_max and
                        biome.mystical_min <= mystical <= biome.mystical_max):
                        self.grid[y][x] = biome
                        break

    def _get_tile_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Get the grid coordinates of the tile at the given screen position."""
        x = int((pos[0] - self.offset_x) / self.cell_size)
        y = int((pos[1] - self.offset_y) / self.cell_size)
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return (x, y)
        return None

    def draw(self, surface: pygame.Surface):
        # Draw grid background and biomes
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(
                    x * self.cell_size + self.offset_x,
                    y * self.cell_size + self.offset_y,
                    self.cell_size,
                    self.cell_size
                )
                
                # Draw cell background
                pygame.draw.rect(surface, (50, 50, 50), rect)
                pygame.draw.rect(surface, (30, 30, 30), rect, 1)
                
                # Draw biome if present
                biome = self.grid[y][x]
                if biome:
                    # Draw biome color
                    pygame.draw.rect(surface, biome.color, rect)

        # Draw tooltip if hovering over a tile with a biome
        if self.hovered_tile:
            x, y = self.hovered_tile
            biome = self.grid[y][x]
            if biome:
                # Create tooltip text
                text = self.font.render(biome.name, True, (255, 255, 255))
                text_rect = text.get_rect()
                
                # Position tooltip above the tile
                tooltip_x = x * self.cell_size + self.offset_x
                tooltip_y = y * self.cell_size + self.offset_y - text_rect.height - 5
                
                # Ensure tooltip stays within screen bounds
                if tooltip_y < 0:
                    tooltip_y = y * self.cell_size + self.offset_y + self.cell_size + 5
                
                # Draw tooltip background
                bg_rect = pygame.Rect(
                    tooltip_x - 5,
                    tooltip_y - 2,
                    text_rect.width + 10,
                    text_rect.height + 4
                )
                pygame.draw.rect(surface, (0, 0, 0), bg_rect)
                pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
                
                # Draw tooltip text
                surface.blit(text, (tooltip_x, tooltip_y))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.offset_x += dx
                self.offset_y += dy
                self.last_mouse_pos = event.pos
            else:
                # Update hovered tile
                self.hovered_tile = self._get_tile_at_pos(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            # Get current mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate grid position under mouse
            grid_x = (mouse_x - self.offset_x) / self.cell_size
            grid_y = (mouse_y - self.offset_y) / self.cell_size
            
            # Store old cell size for calculations
            old_cell_size = self.cell_size
            
            # Update cell size
            zoom_factor = 1.1 if event.y > 0 else 0.9
            self.cell_size = max(10, min(50, self.cell_size * zoom_factor))
            
            # Adjust offset to zoom towards mouse position
            self.offset_x = mouse_x - grid_x * self.cell_size
            self.offset_y = mouse_y - grid_y * self.cell_size 