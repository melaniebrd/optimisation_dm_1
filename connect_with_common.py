# Tiles values
TILES = [0, 1, 3, 5, 7, 15]

# Each tile can be rotated by 0°, 1 * 90°, 2 * 90°, or 3 * 90° ==> 4 possible rotations
NUMBER_OF_ROTATION = 4
ROTATIONS = range(NUMBER_OF_ROTATION)

# Possible values for each connection
CONNECTION = [0, 1]


def rotate(tile):
    return (tile << 1) & (14) | (tile >> 3) & 1 


def possible_tiles():
        """
        Build a dictionary {} with for each tile, the value of the tile after a rotation of 0, 1 * 90°, 2 * 90°, and 3 * 90°
        Ex : {1: [1, 2, 4, 8], 3: [3, 6, 12, 9]} 
        """
        rotated_tiles = {tile : [tile] for tile in TILES}
        for tile in TILES:
            for _ in range(1, NUMBER_OF_ROTATION):
                last_rotated_tile = rotated_tiles[tile][-1]
                newly_rotated_tile = rotate(last_rotated_tile)
                rotated_tiles[tile].append(newly_rotated_tile)
        return rotated_tiles


class PossibleTiles:

    class __PossibleTiles:

        def __init__(self):
            self.values = possible_tiles()

        def __str__(self):
            return repr(self) + self.values

    instance = None

    def __init__(self):
        if not PossibleTiles.instance:
            PossibleTiles.instance = PossibleTiles.__PossibleTiles()

    def __getattr__(self, name):
        return getattr(self.instance, name)