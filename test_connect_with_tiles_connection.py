from connect_with_tiles_connection import possible_connection_between_tiles

# nose-parameterized from : https://github.com/wolever/nose-parameterized
from nose.tools import assert_equal
from nose_parameterized import parameterized  

import unittest


class TestConnect(unittest.TestCase):

    @parameterized.expand([
        (1, 3, 8, 2, True, True),
        (1, 5, 8, 2, False, True),
        (15, 1, 8, 2, True, True),
        (15, 1, 8, 2, True, True),
        (0, 8, 8, 2, True, False),
        ])
    def test_has_connection_at_position(self, tile_1, tile_2, position_1, position_2, constraint, expected_boolean):
        assert_equal(
            possible_connection_between_tiles(
                tile_1, 
                tile_2, 
                position_1, 
                position_2, 
                constraint
            ),
            expected_boolean
        )


if __name__ == "__main__":
    unittest.main()