from math import isclose

from hypothesis import assume, given

from utils import vectors


@given(x=vectors())
def test_normalize_length(x):
    """x.normalize().length == 1 and x == x.length * x.normalize()"""
    assume(x != (0, 0))
    assert isclose(x.normalize().length, 1)
    assert x.isclose(x.length * x.normalize())
