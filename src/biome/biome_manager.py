import json
from src.biome.biome import Biome
from src.ressources.ressource import Resource

class BiomeManager:
    def __init__(self, file_path):
        self.biomes = []
        self.load_biomes(file_path)

    def load_biomes(self, file_path):
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # For each biome entry in the JSON
        for biome_data in data:
            # Create Resource object
            resource = Resource(biome_data["resource_type"], biome_data["resource_variant"])
            
            # Create Biome object and store it in the list
            biome = Biome(
                name=biome_data["name"],
                height_min=biome_data["height_min"],
                height_max=biome_data["height_max"],
                humidity_min=biome_data["humidity_min"],
                humidity_max=biome_data["humidity_max"],
                temperature_min=biome_data["temperature_min"],
                temperature_max=biome_data["temperature_max"],
                mystical_min=biome_data["mystical_min"],
                mystical_max=biome_data["mystical_max"],
                resource=resource
            )
            self.biomes.append(biome)

    def __repr__(self):
        return f"BiomeManager(biomes={self.biomes})"
