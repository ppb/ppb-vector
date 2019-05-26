from math import isinf

import pytest  # type: ignore
from hypothesis import assume, given, note

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
def test_reflect_involutive(initial: Vector, normal: Vector):
    """Test that reflection is its own inverse

    initial.reflect(normal).reflect(normal) ≃ initial
    """
    assert initial.isclose( initial.reflect(normal).reflect(normal) )


@given(initial=vectors(), normal=units())
def test_reflect_prop(initial: Vector, normal: Vector):
    """Test several properties of Vector.reflect

    * initial.reflect(normal) * normal == - initial * normal
    * normal.angle(initial) == 180 - normal.angle(reflected)
    """
    # Exclude cases where the initial vector is very close to the surface
    assume(not angle_isclose(initial.angle(normal) % 180, 90, epsilon=10))

    # Exclude cases where the initial vector is very small
    assume(initial.length > 1e-10)

    reflected = initial.reflect(normal)
    returned = reflected.reflect(normal)
    note(f"|normal|: {normal.length}, |initial|: {initial.length}")
    note(f"angle(normal, initial): {normal.angle(initial)}")
    note(f"angle(normal, reflected): {normal.angle(reflected)}")
    note(f"Reflected: {reflected}")
    assert not any(map(isinf, reflected))
    note(f"initial ⋅ normal: {initial * normal}")
    note(f"reflected ⋅ normal: {reflected * normal}")
    assert isclose((initial * normal), -(reflected * normal))
    assert angle_isclose(normal.angle(initial), 180 - normal.angle(reflected))
