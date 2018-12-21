import pytest  # type: ignore
from hypothesis import assume, given
from hypothesis.strategies import floats
from math import isclose
from utils import angle_isclose, vectors

from ppb_vector import Vector2


@given(x=vectors(max_magnitude=1e75), l=floats(min_value=-1e75, max_value=1e75))
def test_scale_to_length(x: Vector2, l: float):
    """Test that the length of x.scale_to(l) is l."""
    try:
        assert isclose(x.scale_to(l).length, l)
    except ZeroDivisionError:
        assert x == (0, 0)
    except ValueError:
        assert l < 0


@given(x=vectors(max_magnitude=1e75), length=floats(min_value=0, max_value=1e75))
def test_scale_aligned(x: Vector2, length: float):
    """Test that the length of x.scale_to(length) is length."""
    assume(length > 0)
    try:
        assert angle_isclose(x.scale_to(length).angle(x), 0)
    except ZeroDivisionError:
        assert x == (0, 0)
