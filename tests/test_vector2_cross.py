from ppb_vector import Vector2
from hypothesis import given, strategies as st
from math import isclose
from numbers import Real
from utils import vectors
import pytest  # type: ignore

@pytest.mark.parametrize("left, right, expected", [
    (Vector2(1, 1), Vector2(0, -1), -1),
    (Vector2(1, 1), Vector2(-1, 0), 1),
    (Vector2(0, 1), Vector2(0, -1), 0),
    (Vector2(-1, -1), Vector2(1, 0), 1),
    (Vector2(-1, -1), Vector2(-1, 0), -1)
])
def test_cross(left, right, expected):
    assert left ^ right == expected
    assert right ^ left == -expected


@given(a=vectors(max_magnitude=1e150), c=vectors(max_magnitude=1e150),
       b=vectors(max_magnitude=1e75),
       l=st.floats(min_value=-1e75,max_value=1e75),
)
def test_cross_linearity(a: Vector2, b: Vector2, c: Vector2, l: Real):
    assert isclose(
        a ^ (l * b + c),
        l * (a ^ b) + (a ^ c)
    )

@given(a=vectors(max_magnitude=1e150), b=vectors(max_magnitude=1e150))
def test_cross_antisymetry(a: Vector2, b: Vector2):
    assert isclose(a ^ b, - b ^ a)
