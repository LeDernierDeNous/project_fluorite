from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum
from ui.style import ColorPalette

@dataclass
class MapConfig:
    """Configuration for map settings."""
    width: int = 400
    height: int = 200
    tile_size: int = 16

@dataclass
class WindowConfig:
    """Configuration for window settings."""
    width: int = 1280
    height: int = 720

@dataclass
class UIConfig:
    """Configuration for UI settings."""
    background_color: Tuple[int, int, int] = (0, 0, 0)
    menu_background_color: Tuple[int, int, int] = (50, 50, 50)
    button_width: int = 200
    button_height: int = 50
    button_color: Tuple[int, int, int] = (100, 100, 100)
    button_hover_color: Tuple[int, int, int] = (150, 150, 150)
    button_text_color: Tuple[int, int, int] = (255, 255, 255)

class Config:
    """Main configuration class that manages all game settings.
    
    This class provides a centralized location for all game configuration settings,
    organized into logical groups using dataclasses.
    """
    
    def __init__(self) -> None:
        """Initialize the configuration with default values."""
        self._map_config = MapConfig()
        self._window_config = WindowConfig()
        self._ui_config = UIConfig()
        self._theme = ColorPalette.DARK

    @property
    def map_config(self) -> MapConfig:
        """Get the map configuration.
        
        Returns:
            MapConfig: The current map configuration
        """
        return self._map_config

    @property
    def window_config(self) -> WindowConfig:
        """Get the window configuration.
        
        Returns:
            WindowConfig: The current window configuration
        """
        return self._window_config

    @property
    def ui_config(self) -> UIConfig:
        """Get the UI configuration.
        
        Returns:
            UIConfig: The current UI configuration
        """
        return self._ui_config

    @property
    def theme(self) -> ColorPalette:
        """Get the current theme.
        
        Returns:
            ColorPalette: The current color theme
        """
        return self._theme

    @theme.setter
    def theme(self, value: ColorPalette) -> None:
        """Set the current theme.
        
        Args:
            value: The new color theme to use
        """
        self._theme = value

    def get_map_dimensions(self) -> Tuple[int, int]:
        """Get the map dimensions.
        
        Returns:
            Tuple[int, int]: The width and height of the map
        """
        return self._map_config.width, self._map_config.height

    def get_window_dimensions(self) -> Tuple[int, int]:
        """Get the window dimensions.
        
        Returns:
            Tuple[int, int]: The width and height of the window
        """
        return self._window_config.width, self._window_config.height

    def get_tile_size(self) -> int:
        """Get the tile size.
        
        Returns:
            int: The size of each tile in pixels
        """
        return self._map_config.tile_size

    def validate(self) -> bool:
        """Validate the current configuration.
        
        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        # Validate map dimensions
        if self._map_config.width <= 0 or self._map_config.height <= 0:
            return False
            
        # Validate window dimensions
        if self._window_config.width <= 0 or self._window_config.height <= 0:
            return False
            
        # Validate tile size
        if self._map_config.tile_size <= 0:
            return False
            
        # Validate UI dimensions
        if self._ui_config.button_width <= 0 or self._ui_config.button_height <= 0:
            return False
            
        return True
