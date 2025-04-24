import pygame
from typing import Optional
from ..core.scene import Scene
from ..components import Button
from ..style.style_manager import StyleManager, FontSize
from map.map_manager import MapManager
from biome.biome_loader import BiomeLoader
from biome.biome_map import BiomeMap

class GameScreen(Scene):
    """Game screen scene.
    
    This scene displays the game map and handles map interactions.
    It manages the map rendering, user interactions, and provides
    a menu button to return to the title screen.
    """
    
    def __init__(self, config) -> None:
        """Initialize the game screen.
        
        Args:
            config: Game configuration object
        """
        super().__init__(config)
        self._style = StyleManager.get_instance().get_style()
        self._biome_loader = BiomeLoader()
        self._biome_map: Optional[BiomeMap] = None
        self._menu_button: Optional[Button] = None
        self._setup_ui()
        self._initialize_map()
        
    def _setup_ui(self) -> None:
        """Setup the game screen UI components."""
        # Get current window dimensions
        width, height = self._config.get_window_dimensions()
        
        # Calculate dimensions relative to window size
        button_width = min(width // 8, 100)
        button_height = min(height // 16, 40)
        margin = min(width, height) // 60  # Responsive margin
        
        # Create menu button - position in top-left with responsive margin
        self._menu_button = Button(
            x=margin,
            y=margin,
            width=button_width,
            height=button_height,
            text="Menu",
            action=self._on_menu_clicked,
            color_type="secondary",
            hover_color_type="hover",
            text_color_type="text"
        )
        
    def _on_menu_clicked(self) -> None:
        """Handle menu button click event."""
        self._next_scene = "title"
        
    def _initialize_map(self) -> None:
        """Initialize the biome map if not already done."""
        if not self._biome_map:
            self._biome_loader.load()
            self._biome_map = BiomeMap(self._biome_loader.biomes)
            # Update map dimensions with current window size
            width, height = self._config.get_window_dimensions()
            self._biome_map.update_screen_size(width, height)
        
    def on_window_resize(self, width: int, height: int) -> None:
        """Handle window resize event.
        
        Args:
            width: New window width
            height: New window height
        """
        # Update UI components for new window size
        self._setup_ui()
        # Update map dimensions if it exists
        if self._biome_map:
            self._biome_map.update_screen_size(width, height)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.
        
        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.VIDEORESIZE:
            # Update UI components for new window size
            self._setup_ui()
            if self._biome_map:
                self._biome_map.update_screen_size(event.w, event.h)
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._menu_button and self._menu_button.is_clicked(event.pos):
                self._menu_button.on_click()
                
        if self._biome_map:
            self._biome_map.handle_event(event)
            
    def update(self) -> None:
        """Update the game screen state."""
        if not self._biome_map:
            self._initialize_map()
            
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the game screen.
        
        Args:
            surface: Surface to draw on
        """
        # Draw background
        surface.fill(self._style.get_color("background"))
        
        # Draw map
        if self._biome_map:
            self._biome_map.draw(surface)
            
        # Draw UI components
        if self._menu_button:
            self._menu_button.draw(surface)
            
    def reset(self) -> None:
        """Reset the game screen state."""
        super().reset()
        self._biome_map = None 