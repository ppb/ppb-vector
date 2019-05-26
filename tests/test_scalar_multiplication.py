from hypothesis import assume, given, strategies as st
from pytest import raises  # type: ignore

from ppb_vector import Vector
from utils import floats, isclose, vectors


@given(scalar=floats(), v=vectors())
def test_scalar_coordinates(scalar: float, v: Vector):
    assert scalar * v.x == (scalar * v).x
    assert scalar * v.y == (scalar * v).y


@given(scalar1=floats(), scalar2=floats(), v=vectors())
def test_scalar_associative(scalar1: float, scalar2: float, v: Vector):
    """(scalar1 * scalar2) * v == scalar1 * (scalar2 * v)"""
    left = (scalar1 * scalar2) * v
    right = scalar1 * (scalar2 * v)
    assert left.isclose(right)


@given(scalar=floats(), v=vectors(), w=vectors())
def test_scalar_linear(scalar: float, v: Vector, w: Vector):
    assert (scalar * (v + w)).isclose(
        scalar * v + scalar * w,
        rel_to=[v, w, scalar * v, scalar * w],
    )


@given(scalar=floats(), v=vectors())
def test_scalar_length(scalar: float, v: Vector):
    assert isclose((scalar * v).length, abs(scalar) * v.length)


@given(v=vectors(), scalar=floats())
def test_scalar_division(v: Vector, scalar: float):
    """Test that (v / λ) = (1 / λ) * v"""
    assume(abs(scalar) > 1e-100)
    assert (v / scalar).isclose((1 / scalar) * v)


@given(v=vectors(), scalar=floats())
def test_scalar_inverse(v: Vector, scalar: float):
    """Test that (λ * v / λ) ≃ v"""
    assume(abs(scalar) > 1e-100)
    assert v.isclose(scalar * v / scalar)


@given(v=vectors(), scalar=floats())
def test_scalar_rmul(v: Vector, scalar: float):
    assert scalar * v == v.scale_by(scalar)


@given(v=vectors(), scalar=st.integers())
def test_integer_multiplication(v: Vector, scalar: int):
    assert scalar * v == float(scalar) * v


@given(v=vectors(), scalar=st.integers())
def test_integer_division(v: Vector, scalar: int):
    assume(scalar != 0)
    assert v / scalar == v / float(scalar)


@given(v=vectors())
def test_division_by_zero(v: Vector):
    with raises(ZeroDivisionError):
        v / 0

    with raises(ZeroDivisionError):
        v / 0.
