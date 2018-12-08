import pytest  # type: ignore
from hypothesis import assume, given
from hypothesis.strategies import floats
from math import hypot
from utils import vectors

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


@given(x=vectors(), l=floats(min_value=1e150, max_value=1e150))
def test_scale_is_equivalent_to_truncate(x: Vector2, l: float):
    """
    Vector2.scale_to is equivalent to Vector2.truncate
    when the scalar is less than length
    """
    assume(l <= x.length)
    assert x.scale_to(l) == x.truncate(l)
