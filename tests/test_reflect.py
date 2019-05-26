from math import isinf, isnan

import pytest  # type: ignore
from hypothesis import assume, given

from ppb_vector import Vector
from utils import angle_isclose, isclose, units, vectors


reflect_data = (
    (Vector(1, 1), Vector(0, -1), Vector(1, -1)),
    (Vector(1, 1), Vector(-1, 0), Vector(-1, 1)),
    (Vector(0, 1), Vector(0, -1), Vector(0, -1)),
    (Vector(-1, -1), Vector(1, 0), Vector(1, -1)),
    (Vector(-1, -1), Vector(-1, 0), Vector(1, -1)),
)


@pytest.mark.parametrize("initial, surface_normal, expected", reflect_data)
def test_reflect(initial, surface_normal, expected):
    assert initial.reflect(surface_normal).isclose(expected)


@given(initial=vectors(), normal=units())
def test_reflect_nan_inf(initial: Vector, normal: Vector):
    """Test that reflection doesn't produce NaN or ±∞."""
    assert not any(isinf(c) or isnan(c) for c in initial.reflect(normal))


@given(initial=vectors(), normal=units())
def test_reflect_length(initial: Vector, normal: Vector):
    """Test that reflection preserve lengths."""
    assert isclose(initial.length, initial.reflect(normal).length)


@given(initial=vectors(), normal=units())
def test_reflect_involutive(initial: Vector, normal: Vector):
    """Test that reflection is its own inverse

    initial.reflect(normal).reflect(normal) ≃ initial
    """
    assert initial.isclose(initial.reflect(normal).reflect(normal))


@given(initial=vectors(), normal=units())
def test_reflect_angle(initial: Vector, normal: Vector):
    """Test angle-related properties of Vector.reflect:

    * initial.reflect(normal) * normal == - initial * normal
    * normal.angle(initial) == 180 - normal.angle(reflected)
    """
    # Exclude initial vectors that are very small or very close to the surface.
    assume(not angle_isclose(initial.angle(normal) % 180, 90, epsilon=10))
    assume(initial.length > 1e-10)

    reflected = initial.reflect(normal)
    assert isclose((initial * normal), -(reflected * normal))
    assert angle_isclose(normal.angle(initial), 180 - normal.angle(reflected))
