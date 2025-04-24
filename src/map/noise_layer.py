from dataclasses import dataclass
from typing import List, Optional, Tuple
import noise
import random

@dataclass
class NoiseParameters:
    """Parameters for noise generation."""
    octaves: int
    persistence: float
    lacunarity: float
    scale_factor: float = 1.0

class BaseNoiseLayer:
    """Base class for all noise layers.
    
    This class provides the foundation for generating different types of noise maps
    using Perlin noise. Subclasses should implement their specific noise generation
    logic by overriding the _generate method.
    """
    
    def __init__(self, width: int, height: int, scale: float = 50.0) -> None:
        """Initialize the noise layer.
        
        Args:
            width: Width of the noise map
            height: Height of the noise map
            scale: Scale factor for noise generation
        """
        self._width = width
        self._height = height
        self._scale = scale
        self._seed = random.randint(0, 100000)
        self._map: Optional[List[List[float]]] = None
        self._generate_map()

    def _generate_map(self) -> None:
        """Generate the noise map."""
        self._map = self._generate()

    def _generate(self) -> List[List[float]]:
        """Generate the noise values.
        
        Returns:
            List[List[float]]: 2D array of noise values
        """
        raise NotImplementedError("Subclasses must implement _generate")

    def get(self, x: int, y: int) -> float:
        """Get the noise value at the specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            float: Noise value normalized to range [0, 1]
            
        Raises:
            ValueError: If coordinates are out of bounds
        """
        if not (0 <= x < self._width and 0 <= y < self._height):
            raise ValueError(f"Coordinates ({x}, {y}) out of bounds")
            
        if self._map is None:
            self._generate_map()
            
        value = self._map[x][y]
        return (value + 1) / 2  # Convert from [-1, 1] to [0, 1]

    @property
    def width(self) -> int:
        """Get the width of the noise map."""
        return self._width

    @property
    def height(self) -> int:
        """Get the height of the noise map."""
        return self._height

    @property
    def scale(self) -> float:
        """Get the scale factor."""
        return self._scale

    @property
    def seed(self) -> int:
        """Get the random seed."""
        return self._seed

class HeightNoiseLayer(BaseNoiseLayer):
    """Noise layer for height map with sharp peaks and valleys."""
    
    def __init__(self, width: int, height: int, scale: float = 50.0) -> None:
        """Initialize the height noise layer."""
        self._params = NoiseParameters(
            octaves=2,
            persistence=0.8,
            lacunarity=2.0
        )
        super().__init__(width, height, scale)

    def _generate(self) -> List[List[float]]:
        """Generate height noise with sharp peaks and valleys."""
        return [
            [noise.pnoise2(
                (x + self._seed) / self._scale,
                (y + self._seed) / self._scale,
                octaves=self._params.octaves,
                persistence=self._params.persistence,
                lacunarity=self._params.lacunarity
            ) for y in range(self._height)]
            for x in range(self._width)
        ]

class HumidityNoiseLayer(BaseNoiseLayer):
    """Noise layer for humidity with medium-sized patches."""
    
    def __init__(self, width: int, height: int, scale: float = 50.0) -> None:
        """Initialize the humidity noise layer."""
        self._params = NoiseParameters(
            octaves=4,
            persistence=0.5,
            lacunarity=2.0
        )
        super().__init__(width, height, scale)

    def _generate(self) -> List[List[float]]:
        """Generate humidity noise with medium-sized patches."""
        return [
            [noise.pnoise2(
                (x + self._seed) / self._scale,
                (y + self._seed) / self._scale,
                octaves=self._params.octaves,
                persistence=self._params.persistence,
                lacunarity=self._params.lacunarity
            ) for y in range(self._height)]
            for x in range(self._width)
        ]

class TemperatureNoiseLayer(BaseNoiseLayer):
    """Noise layer for temperature with medium-sized patches."""
    
    def __init__(self, width: int, height: int, scale: float = 50.0) -> None:
        """Initialize the temperature noise layer."""
        self._params = NoiseParameters(
            octaves=4,
            persistence=0.5,
            lacunarity=2.0,
            scale_factor=1.2
        )
        super().__init__(width, height, scale)

    def _generate(self) -> List[List[float]]:
        """Generate temperature noise with medium-sized patches."""
        return [
            [noise.pnoise2(
                (x + self._seed) / (self._scale * self._params.scale_factor),
                (y + self._seed) / (self._scale * self._params.scale_factor),
                octaves=self._params.octaves,
                persistence=self._params.persistence,
                lacunarity=self._params.lacunarity
            ) for y in range(self._height)]
            for x in range(self._width)
        ]

class MysticalNoiseLayer(BaseNoiseLayer):
    """Noise layer for mystical with large, smooth blending areas."""
    
    def __init__(self, width: int, height: int, scale: float = 50.0) -> None:
        """Initialize the mystical noise layer."""
        self._params = NoiseParameters(
            octaves=6,
            persistence=0.3,
            lacunarity=2.0,
            scale_factor=0.8
        )
        super().__init__(width, height, scale)

    def _generate(self) -> List[List[float]]:
        """Generate mystical noise with large, smooth blending areas."""
        return [
            [noise.pnoise2(
                (x + self._seed) / (self._scale * self._params.scale_factor),
                (y + self._seed) / (self._scale * self._params.scale_factor),
                octaves=self._params.octaves,
                persistence=self._params.persistence,
                lacunarity=self._params.lacunarity
            ) for y in range(self._height)]
            for x in range(self._width)
        ]
