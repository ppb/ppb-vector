import unittest

import ppb_vector


class TestIterable(unittest.TestCase):

    def test_is_iterable(self):
        test_vector = ppb_vector.Vector2(3, 4)
        test_tuple = tuple(test_vector)
        print(test_tuple)
        self.assertEqual(test_tuple[0], 3)
        self.assertEqual(test_tuple[1], 4)


if __name__ == '__main__':
    unittest.main()
