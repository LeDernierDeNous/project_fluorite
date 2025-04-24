from typing import List, Tuple, Optional
from dataclasses import dataclass
from map.tile import Tile

@dataclass
class MapDimensions:
    """Container for map dimensions."""
    width: int
    height: int
    tile_size: int

class GameMap:
    """Represents a grid-based game map composed of tiles.
    
    This class is responsible for:
    - Managing a grid of tiles
    - Rendering the map
    - Providing access to tiles
    - Handling map dimensions
    """
    
    def __init__(self, width: int, height: int, tile_size: int) -> None:
        """Initialize a new game map.
        
        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            tile_size: Size of each tile in pixels
            
        Raises:
            ValueError: If dimensions are invalid
        """
        if width <= 0 or height <= 0 or tile_size <= 0:
            raise ValueError("Map dimensions and tile size must be positive")
            
        self._dimensions = MapDimensions(
            width=width,
            height=height,
            tile_size=tile_size
        )
        
        self._tiles: List[List[Tile]] = []
        self._initialize_tiles()

    def _initialize_tiles(self) -> None:
        """Initialize the tile grid with empty tiles."""
        spacing = 2  # Space between tiles
        actual_tile_size = self._dimensions.tile_size - spacing
        
        self._tiles = []
        for x in range(0, self._dimensions.width, self._dimensions.tile_size):
            row = []
            for y in range(0, self._dimensions.height, self._dimensions.tile_size):
                tile = Tile(
                    x=x,
                    y=y,
                    size=actual_tile_size,
                    color=(0, 100, 0)  # Default grass color
                )
                row.append(tile)
            self._tiles.append(row)

    def draw(self, surface) -> None:
        """Draw the map on the given surface.
        
        Args:
            surface: Surface to draw on
        """
        for row in self._tiles:
            for tile in row:
                tile.draw(surface)

    def get_tile_at(self, x: int, y: int) -> Optional[Tile]:
        """Get the tile at the specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Optional[Tile]: Tile at the coordinates or None if out of bounds
        """
        if not (0 <= x < self._dimensions.width and 0 <= y < self._dimensions.height):
            return None
            
        tile_x = x // self._dimensions.tile_size
        tile_y = y // self._dimensions.tile_size
        
        if 0 <= tile_x < len(self._tiles) and 0 <= tile_y < len(self._tiles[0]):
            return self._tiles[tile_x][tile_y]
        return None

    def get_tile_at_position(self, pos: Tuple[int, int]) -> Optional[Tile]:
        """Get the tile at the specified position.
        
        Args:
            pos: (x, y) position tuple
            
        Returns:
            Optional[Tile]: Tile at the position or None if out of bounds
        """
        return self.get_tile_at(pos[0], pos[1])

    @property
    def dimensions(self) -> MapDimensions:
        """Get the map dimensions."""
        return self._dimensions

    @property
    def tiles(self) -> List[List[Tile]]:
        """Get the tile grid."""
        return self._tiles.copy()

    def __repr__(self) -> str:
        """Get a string representation of the map."""
        return (
            f"GameMap(width={self._dimensions.width}, "
            f"height={self._dimensions.height}, "
            f"tile_size={self._dimensions.tile_size})"
        )