from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from random import uniform

@dataclass
class BiomeProperties:
    """Container for biome property ranges."""
    height: Tuple[float, float]
    humidity: Tuple[float, float]
    temperature: Tuple[float, float]
    mystical: Tuple[float, float]

@dataclass
class BiomeResources:
    """Container for biome resource information."""
    type: str
    variant: str

class Biome:
    """Represents a biome with specific environmental conditions and resources.
    
    A biome is defined by ranges of environmental factors (height, humidity, temperature, mystical)
    and contains specific resources. The biome can generate random properties within its ranges
    and determine if given environmental conditions match its requirements.
    """
    
    def __init__(self, name: str, height_min: float, height_max: float,
                 humidity_min: float, humidity_max: float,
                 temperature_min: float, temperature_max: float,
                 mystical_min: float, mystical_max: float,
                 resource_type: str, resource_variant: str,
                 color: Tuple[int, int, int]) -> None:
        """Initialize a new biome.
        
        Args:
            name: The name of the biome
            height_min: Minimum height value
            height_max: Maximum height value
            humidity_min: Minimum humidity value
            humidity_max: Maximum humidity value
            temperature_min: Minimum temperature value
            temperature_max: Maximum temperature value
            mystical_min: Minimum mystical value
            mystical_max: Maximum mystical value
            resource_type: Type of resource found in this biome
            resource_variant: Variant of the resource
            color: RGB color tuple for visualization
        """
        self._name = name
        self._properties = BiomeProperties(
            height=(height_min, height_max),
            humidity=(humidity_min, humidity_max),
            temperature=(temperature_min, temperature_max),
            mystical=(mystical_min, mystical_max)
        )
        self._resources = BiomeResources(
            type=resource_type,
            variant=resource_variant
        )
        self._color = color
        
        # Validate property ranges
        self._validate_properties()

    def _validate_properties(self) -> None:
        """Validate that all property ranges are valid.
        
        Raises:
            ValueError: If any property range is invalid
        """
        for prop_name, (min_val, max_val) in self._properties.__dict__.items():
            if min_val > max_val:
                raise ValueError(f"Invalid {prop_name} range: {min_val} > {max_val}")
            if not (0 <= min_val <= 1 and 0 <= max_val <= 1):
                raise ValueError(f"{prop_name} values must be between 0 and 1")

    def generate_properties(self) -> Dict[str, float]:
        """Generate random properties within the biome's ranges.
        
        Returns:
            Dict[str, float]: Dictionary of generated property values
        """
        return {
            "height": uniform(*self._properties.height),
            "humidity": uniform(*self._properties.humidity),
            "temperature": uniform(*self._properties.temperature),
            "mystical": uniform(*self._properties.mystical)
        }
    
    def matches(self, height: float, humidity: float,
                temperature: float, mystical: float) -> bool:
        """Check if the given environmental conditions match this biome.
        
        Args:
            height: Height value to check
            humidity: Humidity value to check
            temperature: Temperature value to check
            mystical: Mystical value to check
            
        Returns:
            bool: True if all values are within the biome's ranges
        """
        return (
            self._properties.height[0] <= height <= self._properties.height[1] and
            self._properties.humidity[0] <= humidity <= self._properties.humidity[1] and
            self._properties.temperature[0] <= temperature <= self._properties.temperature[1] and
            self._properties.mystical[0] <= mystical <= self._properties.mystical[1]
        )

    @property
    def name(self) -> str:
        """Get the biome's name."""
        return self._name

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the biome's color."""
        return self._color

    @property
    def resource_type(self) -> str:
        """Get the biome's resource type."""
        return self._resources.type

    @property
    def resource_variant(self) -> str:
        """Get the biome's resource variant."""
        return self._resources.variant

    def __repr__(self) -> str:
        """Get a string representation of the biome."""
        return (
            f"Biome(name={self._name}, "
            f"height={self._properties.height}, "
            f"humidity={self._properties.humidity}, "
            f"temperature={self._properties.temperature}, "
            f"mystical={self._properties.mystical}, "
            f"resource_type={self._resources.type}, "
            f"resource_variant={self._resources.variant}, "
            f"color={self._color})"
        )