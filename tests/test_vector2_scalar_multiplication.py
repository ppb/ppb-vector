import pytest  # type: ignore
from hypothesis import assume, given
from math import isclose
from utils import floats, vectors

from ppb_vector import Vector2


@given(scalar=floats(), vector=vectors())
def test_scalar_coordinates(scalar: float, vector: Vector2):
    assert scalar * vector.x == (scalar * vector).x
    assert scalar * vector.y == (scalar * vector).y


@given(x=floats(), y=floats(), v=vectors())
def test_scalar_associative(x: float, y: float, v: Vector2):
    """(x * y) * v == x * (y * v)"""
    left  = (x * y) * v
    right =  x * (y * v)
    assert left.isclose(right)

@given(l=floats(), x=vectors(), y=vectors())
def test_scalar_linear(l: float, x: Vector2, y: Vector2):
    assert (l * (x + y)).isclose(l*x + l*y, rel_to=[x, y, l*x, l*y])

@given(l=floats(), x=vectors())
def test_scalar_length(l: float, x: Vector2):
    assert isclose((l * x).length, abs(l) * x.length)


@given(x=vectors(), l=floats())
def test_scalar_division(x: Vector2, l: float):
    """Test that (x / λ) = (1 / λ) * x"""
    assume(abs(l) > 1e-100)
    assert (x / l).isclose((1/l) * x)
