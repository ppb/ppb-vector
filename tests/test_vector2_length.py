import unittest

import ppb_vector


class TestLength(unittest.TestCase):

    def test_valid_params(self):
        vector = ppb_vector.Vector2(6, 8)
        assert vector.length == 10

    def test_valid_params_order_doesnt_matter(self):
        vector = ppb_vector.Vector2(8, 6)
        assert vector.length == 10

    def test_zero(self):
        vector = ppb_vector.Vector2(0, 0)
        assert vector.length == 0

    def test_negative(self):
        vector = ppb_vector.Vector2(-6, -8)
        assert vector.length == 10

    def test_nonperfect_square(self):
        vector = ppb_vector.Vector2(1, 2)
        assert vector.length == 2.23606797749979
