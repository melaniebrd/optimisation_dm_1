#from connect import NUMBER_OF_ROTATION, has_connector_at_position, possible_tiles, rotate
from connect_with_common import PossibleTiles, NUMBER_OF_ROTATION, rotate
from connect_with_tiles_orientation import has_connector_at_position

# nose-parameterized from : https://github.com/wolever/nose-parameterized
from nose.tools import assert_equal
from nose_parameterized import parameterized  

import unittest


class TestConnect(unittest.TestCase):

    def setUp(self):
        pt = PossibleTiles()
        self.tiles = pt.values

    @parameterized.expand([
        (0, [0, 0, 0, 0]),
        (1, [1, 2, 4, 8]),
        (3, [3, 6, 12, 9]),
        (5, [5, 10, 5, 10]),
        (7, [7, 14, 13, 11]),
        (15, [15, 15, 15, 15]),
        ])
    def test_rotate(self, tile, expected_tiles):
        for i in range(1, NUMBER_OF_ROTATION):
            tile = rotate(tile)
            assert_equal(tile, expected_tiles[i])

    @parameterized.expand([
        (0, 2, 2, False),
        (1, 2, 4, True),
        (1, 2, 2, False),
        (3, 1, 2, True),
        (3, 1, 4, True),
        (3, 1, 8, False),
        (3, 3, 1, True),
        (5, 2, 4, True),
        (5, 2, 1, True),
        (5, 2, 8, False),
        ])
    def test_has_connector_at_position(self, tile, rotation, position, expected_boolean):
        assert_equal(has_connector_at_position(self.tiles[tile], rotation, position), expected_boolean)


if __name__ == "__main__":
    unittest.main()