import pytest  # type: ignore
from hypothesis import given
from hypothesis.strategies import floats
from math import isclose
from utils import vectors
from ppb_vector import Vector2


@pytest.mark.parametrize("x, y, expected", [
    (Vector2(6, 1), 0, Vector2(0, 0)),
    (Vector2(6, 1), 2, Vector2(12, 2)),
    (Vector2(0, 0), 3, Vector2(0, 0)),
    (Vector2(-1.5, 2.4), -2, Vector2(3.0, -4.8)),
    (Vector2(1, 2), 0.1, Vector2(0.1, 0.2))
])
def test_scalar_multiplication(x, y, expected):
    assert x * y == expected


@given(
    x=floats(min_value=-1e75, max_value=1e75),
    y=floats(min_value=-1e75, max_value=1e75),
    v=vectors(max_magnitude=1e150)
)
def test_scalar_associative(x: float, y: float, v: Vector2):
    left  = (x * y) * v
    right =  x * (y * v)
    assert left.isclose(right)

@given(
    l=floats(min_value=-1e75, max_value=1e75),
    x=vectors(max_magnitude=1e75),
    y=vectors(max_magnitude=1e75),
)
def test_scalar_linear(l: float, x: Vector2, y: Vector2):
    assert (l * (x + y)).isclose(l*x + l*y)

@given(
    l=floats(min_value=-1e150, max_value=1e150),
    x=vectors(max_magnitude=1e150),
)
def test_scalar_length(l: float, x: Vector2):
    assert isclose((l * x).length, abs(l) * x.length)
