import pygame
from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass
from .biome import Biome
from map.noise_layer import HeightNoiseLayer, HumidityNoiseLayer, TemperatureNoiseLayer, MysticalNoiseLayer
from config import Config
from ui.components.resource_filter import ResourceFilter
from ui.components.noise_map_selector import NoiseMapSelector
from ui.style import StyleManager, FontSize

@dataclass
class MapDimensions:
    """Container for map dimensions."""
    grid_width: int
    grid_height: int
    screen_width: int
    screen_height: int
    cell_size: int

@dataclass
class MapPosition:
    """Container for map position and offset."""
    offset_x: int
    offset_y: int
    last_mouse_pos: Tuple[int, int]

class BiomeMap:
    """Manages and renders a grid of biomes with noise-based generation.
    
    This class is responsible for:
    - Generating and managing biome grid
    - Handling user interaction (panning, zooming)
    - Rendering biomes and noise maps
    - Managing resource filters and noise map selection
    """
    
    def __init__(self, biomes: List[Biome]) -> None:
        """Initialize the biome map.
        
        Args:
            biomes: List of Biome objects to use for generation
        """
        self._biomes = biomes
        self._config = Config()
        self._style = StyleManager.get_instance().get_style()
        
        # Initialize dimensions
        self._dimensions = MapDimensions(
            grid_width=self._config.map_config.width,
            grid_height=self._config.map_config.height,
            screen_width=self._config.get_window_dimensions()[0],
            screen_height=self._config.get_window_dimensions()[1],
            cell_size=self._config.map_config.tile_size
        )
        
        # Initialize position
        self._position = MapPosition(
            offset_x=0,
            offset_y=0,
            last_mouse_pos=(0, 0)
        )
        
        # Initialize state
        self._dragging = False
        self._hovered_tile: Optional[Tuple[int, int]] = None
        
        # Initialize noise maps
        self._noise_maps = {
            "Height": HeightNoiseLayer(self._dimensions.grid_width, self._dimensions.grid_height, scale=20.0),
            "Humidity": HumidityNoiseLayer(self._dimensions.grid_width, self._dimensions.grid_height, scale=15.0),
            "Temperature": TemperatureNoiseLayer(self._dimensions.grid_width, self._dimensions.grid_height, scale=25.0),
            "Mystical": MysticalNoiseLayer(self._dimensions.grid_width, self._dimensions.grid_height, scale=30.0)
        }
        
        # Initialize UI components
        self._initialize_ui_components()
        
        # Generate biome grid
        self._grid = [[None for _ in range(self._dimensions.grid_width)] 
                     for _ in range(self._dimensions.grid_height)]
        self._generate_biome_grid()
        self._center_map()

    def _initialize_ui_components(self) -> None:
        """Initialize UI components for the map."""
        # Resource filter
        self._resource_types = list(set(biome.resource_type for biome in self._biomes))
        self._resource_filter = ResourceFilter(
            x=10,
            y=10,
            resource_types=self._resource_types,
            on_filter_change=self._on_filter_change
        )
        self._active_filters = {resource: True for resource in self._resource_types}
        
        # Noise map selector
        margin = 10
        # Position it in the top-right corner with margin
        self._noise_selector = NoiseMapSelector(
            x=self._dimensions.screen_width - 210 - margin,
            y=margin,
            noise_types=list(self._noise_maps.keys()),
            on_map_change=self._on_noise_map_change
        )
        self._active_noise_maps = {noise_type: False for noise_type in self._noise_maps.keys()}

    def _on_filter_change(self, filters: Dict[str, bool]) -> None:
        """Handle resource filter changes.
        
        Args:
            filters: Dictionary of resource types and their filter states
        """
        self._active_filters = filters

    def _on_noise_map_change(self, active_maps: Dict[str, bool]) -> None:
        """Handle noise map selection changes.
        
        Args:
            active_maps: Dictionary of noise map types and their active states
        """
        self._active_noise_maps = active_maps

    def _find_matching_biome(self, height: float, humidity: float,
                           temperature: float, mystical: float) -> Optional[Biome]:
        """Find the best matching biome for given environmental conditions.
        
        Args:
            height: Height value
            humidity: Humidity value
            temperature: Temperature value
            mystical: Mystical value
            
        Returns:
            Optional[Biome]: Best matching biome or None if no match found
        """
        best_match = None
        best_score = 0.0
        
        for biome in self._biomes:
            score = (
                (1.0 if biome._properties.height[0] <= height <= biome._properties.height[1] else 0.0) +
                (1.0 if biome._properties.humidity[0] <= humidity <= biome._properties.humidity[1] else 0.0) +
                (1.0 if biome._properties.temperature[0] <= temperature <= biome._properties.temperature[1] else 0.0) +
                (1.0 if biome._properties.mystical[0] <= mystical <= biome._properties.mystical[1] else 0.0)
            ) / 4.0
            
            if score > best_score:
                best_score = score
                best_match = biome
        
        return best_match if best_score >= 0.5 else None

    def _generate_biome_grid(self) -> None:
        """Generate the biome grid using noise maps."""
        for y in range(self._dimensions.grid_height):
            for x in range(self._dimensions.grid_width):
                height = self._noise_maps["Height"].get(x, y)
                humidity = self._noise_maps["Humidity"].get(x, y)
                temperature = self._noise_maps["Temperature"].get(x, y)
                mystical = self._noise_maps["Mystical"].get(x, y)
                
                self._grid[y][x] = self._find_matching_biome(
                    height, humidity, temperature, mystical
                )
        
        self._resource_filter.update_resource_stats(self._grid)

    def update_screen_size(self, width: int, height: int) -> None:
        """Update screen dimensions and recenter the map.
        
        Args:
            width: New screen width
            height: New screen height
        """
        self._dimensions.screen_width = width
        self._dimensions.screen_height = height
        
        # Update UI components with consistent margins
        margin = 10
        
        # Reposition resource filter to stay in top-left corner
        self._resource_filter.x = margin
        self._resource_filter.y = margin
        
        # Reposition noise selector to stay in top-right corner
        self._noise_selector.x = width - 210 - margin
        self._noise_selector.y = margin
        
        # Recenter the map
        self._center_map()
        
        # Redraw the map
        self._generate_biome_grid()

    def _center_map(self) -> None:
        """Center the map in the current window."""
        total_width = self._dimensions.grid_width * self._dimensions.cell_size
        total_height = self._dimensions.grid_height * self._dimensions.cell_size
        self._position.offset_x = (self._dimensions.screen_width - total_width) // 2
        self._position.offset_y = (self._dimensions.screen_height - total_height) // 2

    def _get_tile_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Get grid coordinates for a screen position.
        
        Args:
            pos: Screen position (x, y)
            
        Returns:
            Optional[Tuple[int, int]]: Grid coordinates or None if outside grid
        """
        x = int((pos[0] - self._position.offset_x) / self._dimensions.cell_size)
        y = int((pos[1] - self._position.offset_y) / self._dimensions.cell_size)
        
        if 0 <= x < self._dimensions.grid_width and 0 <= y < self._dimensions.grid_height:
            return (x, y)
        return None

    def _get_noise_color(self, value: float) -> Tuple[int, int, int]:
        """Convert noise value to grayscale color.
        
        Args:
            value: Noise value (0-1)
            
        Returns:
            Tuple[int, int, int]: RGB color tuple
        """
        color_value = int(value * 255)
        return (color_value, color_value, color_value)

    def _collect_noise_values(self) -> List[float]:
        """Collect values from the currently active noise map.
        
        Returns:
            List[float]: List of noise values
        """
        active_map = next(
            (map for map, active in self._active_noise_maps.items() if active),
            None
        )
        
        if not active_map:
            return []
            
        values = []
        for y in range(self._dimensions.grid_height):
            for x in range(self._dimensions.grid_width):
                values.append(self._noise_maps[active_map].get(x, y))
        return values

    def _draw_histogram(self, surface: pygame.Surface, values: List[float]) -> None:
        """Draw a histogram of noise values.
        
        Args:
            surface: Surface to draw on
            values: List of noise values to plot
        """
        if not values:
            return
            
        # Histogram parameters
        num_bins = 20
        padding = 10
        width = min(200, self._dimensions.screen_width // 6)  # Scale with screen width
        height = min(100, self._dimensions.screen_height // 8)  # Scale with screen height
        x = self._dimensions.screen_width - width - padding
        y = self._dimensions.screen_height - height - padding
        
        # Create bins
        bins = [0] * num_bins
        for value in values:
            bin_index = min(int(value * num_bins), num_bins - 1)
            bins[bin_index] += 1
            
        # Find max bin value
        max_bin = max(bins) if bins else 1
        
        # Draw background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self._style.get_color("surface"), bg_rect)
        pygame.draw.rect(surface, self._style.get_color("border"), bg_rect, 1)
        
        # Draw title
        title = self._style.get_font(FontSize.SMALL).render(
            "Value Distribution", True, self._style.get_color("text")
        )
        surface.blit(title, (x + padding, y + padding))
        
        # Draw bars
        bar_width = width / num_bins
        for i, count in enumerate(bins):
            bar_height = (count / max_bin) * (height - 40)
            bar_x = x + i * bar_width
            bar_y = y + height - bar_height
            bar_rect = pygame.Rect(bar_x, bar_y, bar_width - 1, bar_height)
            pygame.draw.rect(surface, self._style.get_color("primary"), bar_rect)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the biome map and UI components.
        
        Args:
            surface: Surface to draw on
        """
        # Draw grid
        for y in range(self._dimensions.grid_height):
            for x in range(self._dimensions.grid_width):
                rect = pygame.Rect(
                    x * self._dimensions.cell_size + self._position.offset_x,
                    y * self._dimensions.cell_size + self._position.offset_y,
                    self._dimensions.cell_size,
                    self._dimensions.cell_size
                )
                
                # Draw cell background
                pygame.draw.rect(surface, self._style.get_color("surface"), rect)
                pygame.draw.rect(surface, self._style.get_color("border"), rect, 1)
                
                # Draw content
                if any(self._active_noise_maps.values()):
                    self._draw_noise_map(surface, x, y, rect)
                else:
                    self._draw_biome(surface, x, y, rect)
        
        # Draw UI components
        self._resource_filter.draw(surface)
        self._noise_selector.draw(surface)
        
        # Draw histogram if needed
        if any(self._active_noise_maps.values()):
            values = self._collect_noise_values()
            self._draw_histogram(surface, values)
        
        # Draw tooltip
        if self._hovered_tile:
            self._draw_tooltip(surface)

    def _draw_noise_map(self, surface: pygame.Surface, x: int, y: int, rect: pygame.Rect) -> None:
        """Draw noise map value for a cell.
        
        Args:
            surface: Surface to draw on
            x: Grid x coordinate
            y: Grid y coordinate
            rect: Cell rectangle
        """
        for noise_type, active in self._active_noise_maps.items():
            if active:
                color = self._get_noise_color(self._noise_maps[noise_type].get(x, y))
                pygame.draw.rect(surface, color, rect)
                break

    def _draw_biome(self, surface: pygame.Surface, x: int, y: int, rect: pygame.Rect) -> None:
        """Draw biome for a cell.
        
        Args:
            surface: Surface to draw on
            x: Grid x coordinate
            y: Grid y coordinate
            rect: Cell rectangle
        """
        biome = self._grid[y][x]
        if biome:
            if self._active_filters.get(biome.resource_type, True):
                pygame.draw.rect(surface, biome.color, rect)
            else:
                faded_color = tuple(int(c * 0.3) for c in biome.color)
                pygame.draw.rect(surface, faded_color, rect)

    def _draw_tooltip(self, surface: pygame.Surface) -> None:
        """Draw tooltip for hovered tile.
        
        Args:
            surface: Surface to draw on
        """
        x, y = self._hovered_tile
        biome = self._grid[y][x]
        
        # Create tooltip text
        texts = []
        rects = []
        
        # Add title
        if any(self._active_noise_maps.values()):
            active_map = next(map for map, active in self._active_noise_maps.items() if active)
            value = self._noise_maps[active_map].get(x, y)
            title = f"{active_map} Map: {value:.3f}"
        else:
            title = biome.name if biome else "Empty"
        
        title_text = self._style.get_font(FontSize.BODY).render(
            title, True, self._style.get_color("text")
        )
        texts.append(title_text)
        rects.append(title_text.get_rect())
        
        if biome and not any(self._active_noise_maps.values()):
            # Add environment info
            env_text = self._style.get_font(FontSize.SMALL).render(
                f"Height: {biome._properties.height[0]:.1f}-{biome._properties.height[1]:.1f} | "
                f"Humidity: {biome._properties.humidity[0]:.1f}-{biome._properties.humidity[1]:.1f} | "
                f"Temp: {biome._properties.temperature[0]:.1f}-{biome._properties.temperature[1]:.1f}",
                True, self._style.get_color("text_secondary")
            )
            texts.append(env_text)
            rects.append(env_text.get_rect())
            
            # Add resources info
            resources_text = self._style.get_font(FontSize.SMALL).render(
                f"Resource: {biome.resource_type} ({biome.resource_variant})",
                True, self._style.get_color("text_secondary")
            )
            texts.append(resources_text)
            rects.append(resources_text.get_rect())
        
        # Calculate tooltip dimensions
        padding = 10
        tooltip_width = max(rect.width for rect in rects) + padding * 2
        tooltip_height = sum(rect.height for rect in rects) + padding * (len(texts) + 1)
        
        # Position tooltip
        tooltip_x = x * self._dimensions.cell_size + self._position.offset_x
        tooltip_y = y * self._dimensions.cell_size + self._position.offset_y - tooltip_height - 5
        
        # Ensure tooltip stays within screen bounds
        if tooltip_y < 0:
            tooltip_y = y * self._dimensions.cell_size + self._position.offset_y + self._dimensions.cell_size + 5
        if tooltip_x + tooltip_width > self._dimensions.screen_width:
            tooltip_x = self._dimensions.screen_width - tooltip_width - 5
        
        # Draw tooltip background
        bg_rect = pygame.Rect(
            tooltip_x - padding,
            tooltip_y - padding,
            tooltip_width,
            tooltip_height
        )
        pygame.draw.rect(surface, self._style.get_color("surface"), bg_rect)
        pygame.draw.rect(surface, self._style.get_color("border"), bg_rect, 1)
        
        # Draw tooltip text
        current_y = tooltip_y
        for text in texts:
            surface.blit(text, (tooltip_x, current_y))
            current_y += text.get_rect().height + padding

    def _handle_zoom(self, event: pygame.event.Event) -> None:
        """Handle mouse wheel zoom events.
        
        Args:
            event: The pygame event containing zoom information
        """
        if event.y > 0:  # Zoom in
            self._dimensions.cell_size = min(
                self._dimensions.cell_size * 1.1,
                self._config.get_tile_size() * 4  # Maximum zoom level
            )
        else:  # Zoom out
            self._dimensions.cell_size = max(
                self._dimensions.cell_size / 1.1,
                self._config.get_tile_size() / 4  # Minimum zoom level
            )
        
        # Recenter the map after zooming
        self._center_map()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            Optional[str]: State change request or None
        """
        # Handle UI component events
        self._resource_filter.handle_event(event)
        self._noise_selector.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._dragging = True
                self._position.last_mouse_pos = event.pos
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self._dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self._dragging:
                dx = event.pos[0] - self._position.last_mouse_pos[0]
                dy = event.pos[1] - self._position.last_mouse_pos[1]
                self._position.offset_x += dx
                self._position.offset_y += dy
                self._position.last_mouse_pos = event.pos
            else:
                self._hovered_tile = self._get_tile_at_pos(event.pos)
                
        elif event.type == pygame.MOUSEWHEEL:
            self._handle_zoom(event)
            
        return None 