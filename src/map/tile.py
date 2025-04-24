import pygame
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from biome.biome import Biome

@dataclass
class TileProperties:
    """Container for tile properties."""
    height: float
    humidity: float
    temperature: float
    mystical: float

class Tile:
    """Represents a single tile in the game map.
    
    A tile is defined by its position, biome, and environmental properties.
    It can render itself and provide information about its state.
    """
    
    def __init__(self, x: int, y: int, biome: Biome) -> None:
        """Initialize a new tile.
        
        Args:
            x: X coordinate in the grid
            y: Y coordinate in the grid
            biome: Biome associated with this tile
            
        Raises:
            ValueError: If coordinates are negative
        """
        if x < 0 or y < 0:
            raise ValueError("Tile coordinates must be non-negative")
            
        self._x = x
        self._y = y
        self._biome = biome
        self._properties = self._generate_properties()

    def _generate_properties(self) -> TileProperties:
        """Generate environmental properties for the tile.
        
        Returns:
            TileProperties: Generated properties
        """
        props = self._biome.generate_properties()
        return TileProperties(
            height=props["height"],
            humidity=props["humidity"],
            temperature=props["temperature"],
            mystical=props["mystical"]
        )

    def render(self, screen: pygame.Surface, tile_size: int) -> None:
        """Render the tile on the screen.
        
        Args:
            screen: Surface to render on
            tile_size: Size of the tile in pixels
        """
        rect = pygame.Rect(
            self._x * tile_size,
            self._y * tile_size,
            tile_size,
            tile_size
        )
        pygame.draw.rect(screen, self._biome.color, rect)

    @property
    def x(self) -> int:
        """Get the tile's x coordinate."""
        return self._x

    @property
    def y(self) -> int:
        """Get the tile's y coordinate."""
        return self._y

    @property
    def biome(self) -> Biome:
        """Get the tile's biome."""
        return self._biome

    @property
    def properties(self) -> TileProperties:
        """Get the tile's environmental properties."""
        return self._properties

    def get_position(self) -> Tuple[int, int]:
        """Get the tile's position as a tuple.
        
        Returns:
            Tuple[int, int]: (x, y) coordinates
        """
        return (self._x, self._y)

    def __repr__(self) -> str:
        """Get a string representation of the tile."""
        return f"Tile(x={self._x}, y={self._y}, biome={self._biome.name})"
