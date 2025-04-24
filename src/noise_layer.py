import noise
import random

class BaseNoiseLayer:
    def __init__(self, width, height, scale=50.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.seed = random.randint(0, 100000)
        self.map = self._generate()

    def _generate(self):
        raise NotImplementedError("Subclasses must implement _generate")

    def get(self, x, y):
        value = self.map[x][y]
        return (value + 1) / 2  # Convert from -1 to 1 range to 0 to 1 range

class HeightNoiseLayer(BaseNoiseLayer):
    """Noise layer for height map with sharp peaks and valleys"""
    def _generate(self):
        # Use fewer octaves and higher persistence for more dramatic peaks
        return [
            [noise.pnoise2((x + self.seed) / self.scale, (y + self.seed) / self.scale, 
                          octaves=2, persistence=0.8, lacunarity=2.0)
             for y in range(self.height)]
            for x in range(self.width)
        ]

class HumidityNoiseLayer(BaseNoiseLayer):
    """Noise layer for humidity with medium-sized patches"""
    def _generate(self):
        # Medium number of octaves and balanced persistence for natural-looking patches
        return [
            [noise.pnoise2((x + self.seed) / self.scale, (y + self.seed) / self.scale,
                          octaves=4, persistence=0.5, lacunarity=2.0)
             for y in range(self.height)]
            for x in range(self.width)
        ]

class TemperatureNoiseLayer(BaseNoiseLayer):
    """Noise layer for temperature with medium-sized patches"""
    def _generate(self):
        # Similar to humidity but with different seed and scale
        return [
            [noise.pnoise2((x + self.seed) / (self.scale * 1.2), (y + self.seed) / (self.scale * 1.2),
                          octaves=4, persistence=0.5, lacunarity=2.0)
             for y in range(self.height)]
            for x in range(self.width)
        ]

class MysticalNoiseLayer(BaseNoiseLayer):
    """Noise layer for mystical with large, smooth blending areas"""
    def _generate(self):
        # More octaves and lower persistence for smoother transitions
        return [
            [noise.pnoise2((x + self.seed) / (self.scale * 0.8), (y + self.seed) / (self.scale * 0.8),
                          octaves=6, persistence=0.3, lacunarity=2.0)
             for y in range(self.height)]
            for x in range(self.width)
        ]
