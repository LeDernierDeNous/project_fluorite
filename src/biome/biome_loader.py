import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from .biome import Biome

class BiomeLoader:
    """Loads and manages biome definitions from a JSON file.
    
    This class is responsible for:
    - Loading biome definitions from a JSON file
    - Validating the loaded data
    - Creating Biome objects
    - Managing the loaded biomes
    """
    
    def __init__(self, file_path: str = 'biomes.json') -> None:
        """Initialize the biome loader.
        
        Args:
            file_path: Path to the biome definitions JSON file
        """
        self._file_path = Path(file_path)
        self._biomes: List[Biome] = []
        self._logger = logging.getLogger(__name__)

    def load(self) -> List[Biome]:
        """Load biome definitions from the JSON file.
        
        Returns:
            List[Biome]: List of loaded Biome objects
            
        Raises:
            FileNotFoundError: If the biome file doesn't exist
            json.JSONDecodeError: If the JSON file is invalid
            ValueError: If the biome data is invalid
        """
        try:
            if not self._file_path.exists():
                raise FileNotFoundError(f"Biome file not found: {self._file_path}")
                
            with self._file_path.open('r') as f:
                biome_data = json.load(f)
                
            if not isinstance(biome_data, list):
                raise ValueError("Biome data must be a list")
                
            self._biomes = [self._create_biome(biome) for biome in biome_data]
            self._logger.info(f"Successfully loaded {len(self._biomes)} biomes")
            return self._biomes
            
        except FileNotFoundError as e:
            self._logger.error(f"Failed to load biomes: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self._logger.error(f"Invalid JSON format in biome file: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error loading biomes: {str(e)}")
            raise

    def _create_biome(self, biome_data: Dict[str, Any]) -> Biome:
        """Create a Biome object from biome data.
        
        Args:
            biome_data: Dictionary containing biome properties
            
        Returns:
            Biome: Created Biome object
            
        Raises:
            ValueError: If required biome properties are missing or invalid
        """
        try:
            required_fields = {
                'name': str,
                'height_min': float,
                'height_max': float,
                'humidity_min': float,
                'humidity_max': float,
                'temperature_min': float,
                'temperature_max': float,
                'mystical_min': float,
                'mystical_max': float,
                'resource_type': str,
                'resource_variant': str,
                'color': list
            }
            
            # Validate required fields
            for field, field_type in required_fields.items():
                if field not in biome_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(biome_data[field], field_type):
                    raise ValueError(f"Invalid type for {field}: expected {field_type.__name__}")
            
            # Validate color
            color = biome_data['color']
            if len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
                raise ValueError("Color must be a list of 3 integers between 0 and 255")
            
            return Biome(
                name=biome_data['name'],
                height_min=biome_data['height_min'],
                height_max=biome_data['height_max'],
                humidity_min=biome_data['humidity_min'],
                humidity_max=biome_data['humidity_max'],
                temperature_min=biome_data['temperature_min'],
                temperature_max=biome_data['temperature_max'],
                mystical_min=biome_data['mystical_min'],
                mystical_max=biome_data['mystical_max'],
                resource_type=biome_data['resource_type'],
                resource_variant=biome_data['resource_variant'],
                color=tuple(color)
            )
            
        except ValueError as e:
            self._logger.error(f"Invalid biome data: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error creating biome: {str(e)}")
            raise

    @property
    def biomes(self) -> List[Biome]:
        """Get the list of loaded biomes.
        
        Returns:
            List[Biome]: List of loaded Biome objects
        """
        return self._biomes.copy()

    def get_biome_by_name(self, name: str) -> Optional[Biome]:
        """Get a biome by its name.
        
        Args:
            name: Name of the biome to find
            
        Returns:
            Optional[Biome]: Found Biome object or None if not found
        """
        return next((biome for biome in self._biomes if biome.name == name), None)

    def get_biomes_by_resource(self, resource_type: str) -> List[Biome]:
        """Get all biomes that contain a specific resource type.
        
        Args:
            resource_type: Type of resource to search for
            
        Returns:
            List[Biome]: List of biomes containing the resource
        """
        return [biome for biome in self._biomes if biome.resource_type == resource_type] 