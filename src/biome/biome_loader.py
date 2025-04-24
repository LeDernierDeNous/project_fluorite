import json
from .biome import Biome

class BiomeLoader:
    def __init__(self, file_path='biomes.json'):
        self.file_path = file_path
        self.biomes = []

    def load(self):
        try:
            with open(self.file_path, 'r') as f:
                biome_data = json.load(f)
                self.biomes = [self._create_biome(biome) for biome in biome_data]
                return self.biomes
        except FileNotFoundError:
            print("ERROR: biomes.json not found!")
            return []
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON format in biomes.json!")
            return []
        except Exception as e:
            print(f"ERROR: Failed to load biomes: {str(e)}")
            return []

    def _create_biome(self, biome_data):
        return Biome(
            biome_data['name'],
            biome_data['height_min'],
            biome_data['height_max'],
            biome_data['humidity_min'],
            biome_data['humidity_max'],
            biome_data['temperature_min'],
            biome_data['temperature_max'],
            biome_data['mystical_min'],
            biome_data['mystical_max'],
            biome_data['resource_type'],
            biome_data['resource_variant'],
            tuple(biome_data['color'])
        )

    def get_biomes(self):
        return self.biomes 