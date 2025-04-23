import pygame
from typing import List, Tuple, Optional, Dict
from .biome import Biome
from noise_layer import NoiseLayer
from config import Config
from ui.components.resource_filter import ResourceFilter
from ui.components.noise_map_selector import NoiseMapSelector

class BiomeMap:
    def __init__(self, biomes: List[Biome]):
        self.biomes = biomes
        self.config = Config()
        self.cell_size = self.config.TILE_SIZE
        self.grid_width, self.grid_height = self.config.get_map_dimensions()
        self.screen_width, self.screen_height = self.config.get_window_dimensions()
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Tooltip properties
        self.hovered_tile: Optional[Tuple[int, int]] = None
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Resource filter
        self.resource_types = list(set(biome.resource_type for biome in biomes))
        self.resource_filter = ResourceFilter(
            10,  # x position
            10,  # y position
            self.resource_types,
            self._on_filter_change
        )
        self.active_filters = {resource: True for resource in self.resource_types}
        
        # Noise maps
        self.noise_types = ["Height", "Humidity", "Temperature", "Mystical"]
        self.noise_selector = NoiseMapSelector(
            self.screen_width - 210,  # x position (right side)
            10,  # y position
            self.noise_types,
            self._on_noise_map_change
        )
        self.active_noise_maps = {noise_type: False for noise_type in self.noise_types}
        
        # Generate all noise maps with different scales for variety
        self.height_map = NoiseLayer(self.grid_width, self.grid_height, scale=20.0)
        self.humidity_map = NoiseLayer(self.grid_width, self.grid_height, scale=15.0)
        self.temperature_map = NoiseLayer(self.grid_width, self.grid_height, scale=25.0)
        self.mystical_map = NoiseLayer(self.grid_width, self.grid_height, scale=30.0)
        
        # Create a 2D grid to store biome information
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self._generate_biome_grid()
        self._center_map()

    def _on_filter_change(self, filters: Dict[str, bool]):
        self.active_filters = filters

    def _on_noise_map_change(self, active_maps: Dict[str, bool]):
        self.active_noise_maps = active_maps

    def _find_matching_biome(self, height: float, humidity: float, temperature: float, mystical: float) -> Optional[Biome]:
        """Find the best matching biome for the given properties."""
        best_match = None
        best_score = 0
        
        for biome in self.biomes:
            # Calculate how well this biome matches the conditions
            height_match = 1.0 if biome.height_min <= height <= biome.height_max else 0.0
            humidity_match = 1.0 if biome.humidity_min <= humidity <= biome.humidity_max else 0.0
            temperature_match = 1.0 if biome.temperature_min <= temperature <= biome.temperature_max else 0.0
            mystical_match = 1.0 if biome.mystical_min <= mystical <= biome.mystical_max else 0.0
            
            # Calculate overall match score
            match_score = (height_match + humidity_match + temperature_match + mystical_match) / 4.0
            
            # If this biome matches better than the current best, update
            if match_score > best_score:
                best_score = match_score
                best_match = biome
        
        # Only return a biome if it matches at least some conditions
        return best_match if best_score >= 0.5 else None

    def _generate_biome_grid(self):
        # Generate properties for each grid cell using noise maps
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Get all values from noise maps
                height = self.height_map.get(x, y)
                humidity = self.humidity_map.get(x, y)
                temperature = self.temperature_map.get(x, y)
                mystical = self.mystical_map.get(x, y)
                
                # Find the best matching biome
                self.grid[y][x] = self._find_matching_biome(height, humidity, temperature, mystical)
        
        # Update resource statistics after generating the grid
        self.resource_filter.update_resource_stats(self.grid)

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

    def _get_tile_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Get the grid coordinates of the tile at the given screen position."""
        x = int((pos[0] - self.offset_x) / self.cell_size)
        y = int((pos[1] - self.offset_y) / self.cell_size)
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return (x, y)
        return None

    def _get_noise_color(self, value: float) -> Tuple[int, int, int]:
        # Convert noise value (0-1) to grayscale color
        color_value = int(value * 255)
        return (color_value, color_value, color_value)

    def draw(self, surface: pygame.Surface):
        # Draw grid background and biomes/noise maps
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
                
                # Check if any noise map is active
                if any(self.active_noise_maps.values()):
                    # Draw noise maps
                    if self.active_noise_maps["Height"]:
                        height_color = self._get_noise_color(self.height_map.get(x, y))
                        pygame.draw.rect(surface, height_color, rect)
                    elif self.active_noise_maps["Humidity"]:
                        humidity_color = self._get_noise_color(self.humidity_map.get(x, y))
                        pygame.draw.rect(surface, humidity_color, rect)
                    elif self.active_noise_maps["Temperature"]:
                        temp_color = self._get_noise_color(self.temperature_map.get(x, y))
                        pygame.draw.rect(surface, temp_color, rect)
                    elif self.active_noise_maps["Mystical"]:
                        mystical_color = self._get_noise_color(self.mystical_map.get(x, y))
                        pygame.draw.rect(surface, mystical_color, rect)
                else:
                    # Draw biome if present
                    biome = self.grid[y][x]
                    if biome:
                        # Check if biome's resource type is active in filter
                        if self.active_filters.get(biome.resource_type, True):
                            # Draw biome color at full opacity
                            pygame.draw.rect(surface, biome.color, rect)
                        else:
                            # Draw biome color at reduced opacity
                            faded_color = tuple(int(c * 0.3) for c in biome.color)
                            pygame.draw.rect(surface, faded_color, rect)

        # Draw resource filter
        self.resource_filter.draw(surface)
        
        # Draw noise map selector
        self.noise_selector.draw(surface)

        # Draw tooltip if hovering over a tile
        if self.hovered_tile:
            x, y = self.hovered_tile
            biome = self.grid[y][x]
            
            # Create tooltip text
            texts = []
            rects = []
            
            # Add title (biome name or noise map type)
            if any(self.active_noise_maps.values()):
                # Show noise map type and value
                if self.active_noise_maps["Height"]:
                    value = self.height_map.get(x, y)
                    title = f"Height Map: {value:.3f}"
                elif self.active_noise_maps["Humidity"]:
                    value = self.humidity_map.get(x, y)
                    title = f"Humidity Map: {value:.3f}"
                elif self.active_noise_maps["Temperature"]:
                    value = self.temperature_map.get(x, y)
                    title = f"Temperature Map: {value:.3f}"
                elif self.active_noise_maps["Mystical"]:
                    value = self.mystical_map.get(x, y)
                    title = f"Mystical Map: {value:.3f}"
            else:
                # Show biome name
                title = biome.name if biome else "Empty"
            
            title_text = self.font.render(title, True, (255, 255, 255))
            texts.append(title_text)
            rects.append(title_text.get_rect())
            
            if biome:
                # Add environment info if viewing biomes
                if not any(self.active_noise_maps.values()):
                    env_text = self.small_font.render(
                        f"Height: {biome.height_min:.1f}-{biome.height_max:.1f} | "
                        f"Humidity: {biome.humidity_min:.1f}-{biome.humidity_max:.1f} | "
                        f"Temp: {biome.temperature_min:.1f}-{biome.temperature_max:.1f}",
                        True, (200, 200, 200)
                    )
                    texts.append(env_text)
                    rects.append(env_text.get_rect())
                
                # Add resources info
                resources_text = self.small_font.render(
                    f"Resource: {biome.resource_type} ({biome.resource_variant})",
                    True, (200, 200, 200)
                )
                texts.append(resources_text)
                rects.append(resources_text.get_rect())
            
            # Calculate tooltip dimensions
            padding = 10
            tooltip_width = max(rect.width for rect in rects) + padding * 2
            tooltip_height = sum(rect.height for rect in rects) + padding * (len(texts) + 1)
            
            # Position tooltip
            tooltip_x = x * self.cell_size + self.offset_x
            tooltip_y = y * self.cell_size + self.offset_y - tooltip_height - 5
            
            # Ensure tooltip stays within screen bounds
            if tooltip_y < 0:
                tooltip_y = y * self.cell_size + self.offset_y + self.cell_size + 5
            if tooltip_x + tooltip_width > self.screen_width:
                tooltip_x = self.screen_width - tooltip_width - 5
            
            # Draw tooltip background
            bg_rect = pygame.Rect(
                tooltip_x - padding,
                tooltip_y - padding,
                tooltip_width,
                tooltip_height
            )
            pygame.draw.rect(surface, (0, 0, 0), bg_rect)
            pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
            
            # Draw tooltip text
            current_y = tooltip_y
            for text in texts:
                surface.blit(text, (tooltip_x, current_y))
                current_y += text.get_rect().height + padding

    def handle_event(self, event: pygame.event.Event):
        # Handle resource filter events first
        self.resource_filter.handle_event(event)
        
        # Handle noise map selector events
        self.noise_selector.handle_event(event)

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