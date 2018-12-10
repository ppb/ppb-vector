import pytest  # type: ignore
from hypothesis import assume, given
from math import isclose
from utils import vectors
import ppb_vector


@given(v=vectors())
def test_normalize_length(v):
    assume(v != (0, 0))
    assert isclose(v.normalize().length, 1)
    assert v.isclose(v.length * v.normalize())
