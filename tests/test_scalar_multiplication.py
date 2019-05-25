from math import isclose

from hypothesis import assume, given, strategies as st
from pytest import raises  # type: ignore

from ppb_vector import Vector
from utils import floats, vectors


@given(scalar=floats(), vector=vectors())
def test_scalar_coordinates(scalar: float, vector: Vector):
    assert scalar * vector.x == (scalar * vector).x
    assert scalar * vector.y == (scalar * vector).y


@given(scalar1=floats(), scalar2=floats(), x=vectors())
def test_scalar_associative(scalar1: float, scalar2: float, x: Vector):
    """(scalar1 * scalar2) * x == scalar1 * (scalar2 * x)"""
    left = (scalar1 * scalar2) * x
    right = scalar1 * (scalar2 * x)
    assert left.isclose(right)


@given(scalar=floats(), x=vectors(), y=vectors())
def test_scalar_linear(scalar: float, x: Vector, y: Vector):
    assert (scalar * (x + y)).isclose(
        scalar * x + scalar * y,
        rel_to=[x, y, scalar * x, scalar * y],
    )


@given(scalar=floats(), x=vectors())
def test_scalar_length(scalar: float, x: Vector):
    assert isclose((scalar * x).length, abs(scalar) * x.length)


@given(x=vectors(), scalar=floats())
def test_scalar_division(x: Vector, scalar: float):
    """Test that (x / λ) = (1 / λ) * x"""
    assume(abs(scalar) > 1e-100)
    assert (x / scalar).isclose((1 / scalar) * x)


@given(x=vectors(), scalar=floats())
def test_scalar_inverse(x: Vector, scalar: float):
    """Test that (λ * x / λ) ≃ x"""
    assume(abs(scalar) > 1e-100)
    assert x.isclose(scalar * x / scalar)


@given(x=vectors(), scalar=floats())
def test_scalar_rmul(x: Vector, scalar: float):
    assert scalar * x == x.scale_by(scalar)


@given(x=vectors(), scalar=st.integers())
def test_integer_multiplication(x: Vector, scalar: int):
    assert scalar * x == float(scalar) * x


@given(x=vectors(), scalar=st.integers())
def test_integer_division(x: Vector, scalar: int):
    assume(scalar != 0)
    assert x / scalar == x / float(scalar)


@given(x=vectors())
def test_division_by_zero(x: Vector):
    with raises(ZeroDivisionError):
        x / 0

    with raises(ZeroDivisionError):
        x / 0.
