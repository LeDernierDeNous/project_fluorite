import noise
import random

class NoiseLayer:
    def __init__(self, width, height, scale=50.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.seed = random.randint(0, 100000)
        self.map = self._generate()

    def _generate(self):
        return [
            [noise.pnoise2((x + self.seed) / self.scale, (y + self.seed) / self.scale, octaves=6) * 0.5 + 0.5
             for y in range(self.height)]
            for x in range(self.width)
        ]

    def get(self, x, y):
        return self.map[x][y]
