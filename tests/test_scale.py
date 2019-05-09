from math import isclose

from hypothesis import assume, given

from ppb_vector import Vector
from utils import angle_isclose, floats, lengths, vectors


@given(x=vectors(), length=floats())
def test_scale_to_length(x: Vector, length: float):
    """Test that the length of x.scale_to(length) is length.

    Additionally, Vector.scale_to may raise:
    - ZeroDivisionError if the vector is null;
    - ValueError if the desired length is negative.

    """
    try:
        assert isclose(x.scale_to(length).length, length)
    except ZeroDivisionError:
        assert x == (0, 0)
    except ValueError:
        assert length < 0


@given(x=vectors(), length=lengths())
def test_scale_aligned(x: Vector, length: float):
    """Test that x.scale_to(length) is aligned with x."""
    assume(length > 0)
    try:
        assert angle_isclose(x.scale_to(length).angle(x), 0)
    except ZeroDivisionError:
        assert x == (0, 0)
