import pytest  # type: ignore
from hypothesis import assume, given
from math import isclose
from utils import floats, lengths, vectors

from ppb_vector import Vector2


@given(x=vectors(), l=floats())
def test_scale_to_length(x: Vector2, l: float):
    """Test that the length of x.scale_to(l) is l."""
    try:
        assert isclose(x.scale_to(l).length, l)
    except ZeroDivisionError:
        assert x == (0, 0)
    except ValueError:
        assert l < 0
