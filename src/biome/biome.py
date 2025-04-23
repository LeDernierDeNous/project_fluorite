from random import uniform

class Biome:
    def __init__(self, name, height_min, height_max, humidity_min, humidity_max,
                 temperature_min, temperature_max, mystical_min, mystical_max, resource):
        self.name = name
        self.height_min = height_min
        self.height_max = height_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.mystical_min = mystical_min
        self.mystical_max = mystical_max
        self.resource = resource

    def __repr__(self):
        return (f"Biome(name={self.name}, height=({self.height_min}, {self.height_max}), "
                f"humidity=({self.humidity_min}, {self.humidity_max}), "
                f"temperature=({self.temperature_min}, {self.temperature_max}), "
                f"mystical=({self.mystical_min}, {self.mystical_max}), "
                f"resource={self.resource})")

    def generate_properties(self):
        height = uniform(self.height_min, self.height_max)
        humidity = uniform(self.humidity_min, self.humidity_max)
        temperature = uniform(self.temperature_min, self.temperature_max)
        mystical = uniform(self.mystical_min, self.mystical_max)
        return {
            "height": height,
            "humidity": humidity,
            "temperature": temperature,
            "mystical": mystical
        }
    
    def matches(self, height, humidity, temperature, mystical):
        return (
            self.height_range[0] <= height <= self.height_range[1] and
            self.humidity_range[0] <= humidity <= self.humidity_range[1] and
            self.temperature_range[0] <= temperature <= self.temperature_range[1] and
            self.mystical_range[0] <= mystical <= self.mystical_range[1]
        )