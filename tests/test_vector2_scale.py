import pytest
from math import hypot

from ppb_vector import Vector2


@pytest.fixture()
def vector():
    return Vector2(10, 20)


def test_calculate_scale(vector):
    x, y = 10, 20
    length = hypot(x, y)
    scale = 4
    vector_scale_calculated = vector * (scale / length)
    assert vector.scale(scale) == vector_scale_calculated


def test_scale_is_equivalent_to_truncate():
    """ 
    Vector2.scale is equivalent to Vector2.truncate 
    when scalar is less than length
    """
    vector_scale = Vector2(3, 4).scale(4)
    vector_truncate = Vector2(3, 4).truncate(4)
    assert vector_scale == vector_truncate
