from hypothesis import assume, given

from utils import angle_isclose, isclose, vectors


@given(v=vectors())
def test_normalize_length(v):
    """v.normalize().length == 1 and v == v.length * v.normalize()"""
    assume(v)
    assert isclose(v.normalize().length, 1)
    assert v.isclose(v.length * v.normalize())


@given(v=vectors())
def test_normalize_angle(v):
    """Normalization preserves direction."""
    assume(v)
    assert angle_isclose(v.normalize().angle(v), 0)
