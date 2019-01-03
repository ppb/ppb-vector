import pytest  # type: ignore

from ppb_vector import Vector2


def test_is_iterable():
    test_vector = Vector2(3, 4)
    test_tuple = tuple(test_vector)
    assert test_tuple == (3, 4)
