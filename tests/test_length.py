from math import fabs, sqrt

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import floats, isclose, vectors


data = [
    ((6,   8), 10),
    ((8,   6), 10),
    ((0,   0), 0),
    ((-6, -8), 10),
    ((1,   2), sqrt(5)),
]


@pytest.mark.parametrize("v, expected", data,
                         ids=[f"{v}" for v, _ in data])
def test_length(v, expected):
    vector = Vector(v)
    assert vector.length == expected


@given(v=vectors())
def test_length_dot(v: Vector):
    """Test that |v| ≃ √v²."""
    assert isclose(v.length, sqrt(v * v))


@given(v=vectors())
def test_length_zero(v: Vector):
    """1st axiom of normed vector spaces: |v| = 0 iff v = 0"""
    assert (v.length == 0) == not bool(v)


@given(v=vectors(), scalar=floats())
def test_length_scalar(v: Vector, scalar: float):
    """2nd axiom of normed vector spaces: |λv| = |λ| |v|"""
    assert isclose((scalar * v).length, fabs(scalar) * v.length)


@given(v=vectors(), w=vectors())
def test_length_triangle(v: Vector, w: Vector):
    """3rd axiom of normed vector spaces: |v+w| ≤ |v| + |w|"""
    assert (v + w).length <= (1 + 1e-15) * (v.length + w.length)
