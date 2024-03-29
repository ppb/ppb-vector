import operator
from functools import reduce
from math import sqrt

from hypothesis import given, note

from ppb_vector import Vector
from utils import angle_isclose, floats, MAX_MAGNITUDE, units, vectors


# TODO(nicoo): Replace with Vector.zero once #168 is merged.
ZERO = Vector(0, 0)


@given(v=vectors())
def test_decompose_canonical(v: Vector):
    """Decomposition against the canonical (x, y) basis is trivial."""
    x, y = v.decompose((1, 0))

    assert x == (v.x, 0)
    assert y == (0, v.y)


@given(v=vectors(), basis=units())
def test_decompose_recombine(v: Vector, basis: Vector):
    """A vector is the sum of its decomposed components."""
    assert reduce(operator.add, v.decompose(basis)).isclose(v)


@given(v=vectors(), basis=units())
def test_decompose_angles(v: Vector, basis: Vector):
    """Decomposition components are colinear and orthogonal to the basis."""
    a, b = v.decompose(basis)

    assert angle_isclose(basis.angle(a),  0, modulus=180) or a.isclose(ZERO)
    assert angle_isclose(basis.angle(b), 90, modulus=180) or b.isclose(ZERO)


@given(
    basis=units(), v=vectors(),
    # We need |λw| ⩽ MAX_MAGNITUDE; picking |λ| and |w| below √MAX_MAGNITUDE
    #  achieves that, though rejects some otherwise-valid combinations.
    λ=floats(max_magnitude=sqrt(MAX_MAGNITUDE)), w=vectors(sqrt(MAX_MAGNITUDE)),
)
def test_decompose_linear(v: Vector, w: Vector, λ: float, basis: Vector):
    """Decomposition against a fixed basis is linear"""
    inner = (v + λ * w).decompose(basis)
    outer = tuple((t + λ * u for t, u in zip(v.decompose(basis), w.decompose(basis))))

    note(f"inner: {inner}")
    note(f"outer: {outer}")

    assert all((x.isclose(y) for x, y in zip(inner, outer)))
