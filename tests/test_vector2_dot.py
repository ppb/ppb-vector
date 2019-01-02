from ppb_vector import Vector2

from math import sqrt
import pytest  # type: ignore
from hypothesis import assume, given, note
from utils import floats, isclose, vectors


@given(x=vectors(), y=vectors())
def test_dot_commutes(x: Vector2, y: Vector2):
    assert x * y == y * x

@given(x=vectors())
def test_dot_length(x: Vector2):
    assert isclose(x * x, x.length * x.length)


MAGNITUDE=1e10
@given(x=vectors(max_magnitude=MAGNITUDE), z=vectors(max_magnitude=MAGNITUDE),
       y=vectors(max_magnitude=sqrt(MAGNITUDE)),
       scalar=floats(max_magnitude=sqrt(MAGNITUDE)))
def test_dot_linear(x: Vector2, y: Vector2, z: Vector2, scalar: float):
    """Test that x · (λ y + z) = λ x·y + x·z"""
    inner, outer = x * (scalar * y + z), scalar * x * y + x * z
    note(f"inner: {inner}")
    note(f"outer: {outer}")
    assert isclose(inner, outer, rel_tol=1e-5, rel_to=(x, scalar, y, z))


@given(x=vectors(max_magnitude=1e7), y=vectors(max_magnitude=1e7))
def test_dot_from_angle(x: Vector2, y: Vector2):
    """Test x · y == |x| · |y| · cos(θ)"""
    t = x.angle(y)
    cos_t, _ = Vector2._trig(t)

    # Dismiss near-othogonal test inputs
    assume(abs(cos_t) > 1e-6)

    min_len, max_len = sorted((x.length, y.length))
    geometric = min_len * (max_len * cos_t)

    note(f"θ: {t}")
    note(f"cos θ: {cos_t}")
    note(f"algebraic: {x * y}")
    note(f"geometric: {geometric}")
    assert isclose(x * y, geometric, abs_tol=1e-2, rel_tol=1e-4, rel_to=(x, y))
