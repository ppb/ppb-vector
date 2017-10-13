import unittest
from ppb_vector import Vector2


class TestVector2Addition(unittest.TestCase):
    def test_addition_vectors(self):
        test_vector1 = Vector2(1, 0)
        test_vector2 = Vector2(0, 1)
        result = test_vector1 + test_vector2
        self.assertEqual(result, Vector2(1, 1))

    def test_addition_vector_tuple(self):
        test_vector = Vector2(1, 1)
        test_tuple = (2, 4)
        result = test_vector + test_tuple
        self.assertEqual(result, Vector2(3, 5))

    def test_addition_vector_list(self):
        test_vector = Vector2(1, 1)
        test_list = [1, 3]
        result = test_vector + test_list
        self.assertEqual(result, Vector2(2, 4))

    def test_addition_vector_dict(self):
        test_vector = Vector2(1, 1)
        test_dict = {'x': 3, 'y': 5}
        result = test_vector + test_dict
        self.assertEqual(result, Vector2(4, 6))


