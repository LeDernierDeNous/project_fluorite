from map.tile import Tile

class GameMap:
    def __init__(self, width: int, height: int, tile_size: int):
        self.tiles = []
        self.tile_size = tile_size

        for x in range(0, width, tile_size):
            row = []
            for y in range(0, height, tile_size):
                tile = Tile(x, y, tile_size - 2, (0, 100, 0))  # -2 for spacing
                row.append(tile)
            self.tiles.append(row)

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)