import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import noise
from map.tile import Tile
from biome.biome import Biome

@dataclass
class NoiseParameters:
    """Container for noise generation parameters."""
    scale: float
    octaves: int
    repeatx: int
    repeaty: int
    base: int

class MapManager:
    """Manages the generation and rendering of the game map.
    
    This class is responsible for:
    - Generating the map using noise-based terrain
    - Managing biomes and their distribution
    - Rendering the map
    - Providing access to tiles
    """
    
    def __init__(self, width: int, height: int, tile_size: int, biomes: List[Biome]) -> None:
        """Initialize the map manager.
        
        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            tile_size: Size of each tile in pixels
            biomes: List of biomes to use for generation
            
        Raises:
            ValueError: If dimensions are invalid or biomes list is empty
        """
        if width <= 0 or height <= 0 or tile_size <= 0:
            raise ValueError("Map dimensions and tile size must be positive")
        if not biomes:
            raise ValueError("At least one biome must be provided")
            
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._biomes = biomes
        self._tiles: List[List[Tile]] = []
        
        # Noise parameters
        self._noise_params = NoiseParameters(
            scale=50.0,
            octaves=4,
            repeatx=1024,
            repeaty=1024,
            base=0
        )
        
        self.generate_map()

    def generate_map(self) -> None:
        """Generate the map using noise-based terrain generation."""
        self._tiles = []
        
        for y in range(self._height):
            row = []
            for x in range(self._width):
                # Calculate normalized coordinates
                nx = x / self._width - 0.5
                ny = y / self._height - 0.5
                
                # Generate noise values for different properties
                height_val = self._generate_noise(nx, ny, base=0)
                humidity_val = self._generate_noise(nx, ny, base=1)
                temperature_val = self._generate_noise(nx, ny, base=2)
                mystical_val = self._generate_noise(nx, ny, base=3)
                
                # Normalize values to 0-1 range
                height_val = (height_val + 0.5)
                humidity_val = (humidity_val + 0.5)
                temperature_val = (temperature_val + 0.5)
                mystical_val = (mystical_val + 0.5)
                
                # Find matching biome
                biome = self._find_matching_biome(
                    height_val,
                    humidity_val,
                    temperature_val,
                    mystical_val
                )
                
                # Create tile with selected biome
                row.append(Tile(x, y, biome))
                
            self._tiles.append(row)

    def _generate_noise(self, nx: float, ny: float, base: int) -> float:
        """Generate a noise value for the given coordinates.
        
        Args:
            nx: Normalized x coordinate
            ny: Normalized y coordinate
            base: Base value for noise generation
            
        Returns:
            float: Generated noise value
        """
        return noise.pnoise2(
            nx * self._noise_params.scale,
            ny * self._noise_params.scale,
            octaves=self._noise_params.octaves,
            repeatx=self._noise_params.repeatx,
            repeaty=self._noise_params.repeaty,
            base=base
        )

    def _find_matching_biome(self, height: float, humidity: float,
                           temperature: float, mystical: float) -> Biome:
        """Find the best matching biome for the given environmental conditions.
        
        Args:
            height: Height value
            humidity: Humidity value
            temperature: Temperature value
            mystical: Mystical value
            
        Returns:
            Biome: Best matching biome
        """
        # Try to find a matching biome
        for biome in self._biomes:
            if biome.matches(height, humidity, temperature, mystical):
                return biome
                
        # If no biome matches, return a random one as fallback
        return random.choice(self._biomes)

    def render(self, surface) -> None:
        """Render the map on the given surface.
        
        Args:
            surface: Surface to render on
        """
        for row in self._tiles:
            for tile in row:
                rect = (
                    tile.x * self._tile_size,
                    tile.y * self._tile_size,
                    self._tile_size,
                    self._tile_size
                )
                surface.fill(tile.biome.color, rect)

    def get_tile_at_pixel(self, px: int, py: int) -> Optional[Tile]:
        """Get the tile at the specified pixel coordinates.
        
        Args:
            px: Pixel x coordinate
            py: Pixel y coordinate
            
        Returns:
            Optional[Tile]: Tile at the coordinates or None if out of bounds
        """
        tx = px // self._tile_size
        ty = py // self._tile_size
        
        if 0 <= tx < self._width and 0 <= ty < self._height:
            return self._tiles[ty][tx]
        return None

    @property
    def width(self) -> int:
        """Get the map width."""
        return self._width

    @property
    def height(self) -> int:
        """Get the map height."""
        return self._height

    @property
    def tile_size(self) -> int:
        """Get the tile size."""
        return self._tile_size

    @property
    def tiles(self) -> List[List[Tile]]:
        """Get the tile grid."""
        return self._tiles.copy()

    def __repr__(self) -> str:
        """Get a string representation of the map manager."""
        return (
            f"MapManager(width={self._width}, "
            f"height={self._height}, "
            f"tile_size={self._tile_size})"
        )
