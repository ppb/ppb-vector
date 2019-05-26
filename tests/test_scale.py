from hypothesis import assume, given, strategies as st
from pytest import raises  # type: ignore

from ppb_vector import Vector
from utils import angle_isclose, isclose, lengths, vectors


@given(v=vectors(), length=st.floats(max_value=0))
def test_scale_negative_length(v: Vector, length: float):
    """Test that Vector.scale_to raises ValueError on negative lengths."""
    assume(length < 0)
    with raises(ValueError):
        v.scale_to(length)


@given(x=vectors(), length=lengths())
def test_scale_to_length(x: Vector, length: float):
    """Test that the length of x.scale_to(length) is length with x non-null."""
    assume(x != (0, 0))
    assert isclose(x.scale_to(length).length, length)


@given(x=vectors(), length=lengths())
def test_scale_aligned(x: Vector, length: float):
    """Test that x.scale_to(length) is aligned with x."""
    assume(length > 0 and x != (0, 0))
    assert angle_isclose(x.scale_to(length).angle(x), 0)
