from math import isclose

from hypothesis import assume, given

from ppb_vector import Vector2
from utils import floats, vectors


@given(scalar=floats(), vector=vectors())
def test_scalar_coordinates(scalar: float, vector: Vector2):
    assert scalar * vector.x == (scalar * vector).x
    assert scalar * vector.y == (scalar * vector).y


@given(scalar1=floats(), scalar2=floats(), x=vectors())
def test_scalar_associative(scalar1: float, scalar2: float, x: Vector2):
    """(scalar1 * scalar2) * x == scalar1 * (scalar2 * x)"""
    left = (scalar1 * scalar2) * x
    right = scalar1 * (scalar2 * x)
    assert left.isclose(right)


@given(scalar=floats(), x=vectors(), y=vectors())
def test_scalar_linear(scalar: float, x: Vector2, y: Vector2):
    assert (scalar * (x + y)).isclose(
        scalar * x + scalar * y,
        rel_to=[x, y, scalar * x, scalar * y],
    )


@given(scalar=floats(), x=vectors())
def test_scalar_length(scalar: float, x: Vector2):
    assert isclose((scalar * x).length, abs(scalar) * x.length)


@given(x=vectors(), scalar=floats())
def test_scalar_division(x: Vector2, scalar: float):
    """Test that (x / λ) = (1 / λ) * x"""
    assume(abs(scalar) > 1e-100)
    assert (x / scalar).isclose((1 / scalar) * x)
