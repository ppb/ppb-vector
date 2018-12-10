import pytest  # type: ignore
from hypothesis import assume, given
from math import isclose
from utils import vectors
import ppb_vector


@given(x=vectors())
def test_normalize_length(x):
    """x.normalize().length == 1 and x == x.length * x.normalize()"""
    assume(x != (0, 0))
    assert isclose(x.normalize().length, 1)
    assert x.isclose(x.length * x.normalize())
