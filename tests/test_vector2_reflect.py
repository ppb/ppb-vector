from ppb_vector import Vector2
import pytest
from hypothesis import given, assume, note
from math import isclose, isinf
from utils import angle_isclose, units, vectors


reflect_data = (
    (Vector2(1, 1), Vector2(0, -1), Vector2(1, -1)),
    (Vector2(1, 1), Vector2(-1, 0), Vector2(-1, 1)),
    (Vector2(0, 1), Vector2(0, -1), Vector2(0, -1)),
    (Vector2(-1, -1), Vector2(1, 0), Vector2(1, -1)),
    (Vector2(-1, -1), Vector2(-1, 0), Vector2(1, -1))
)


@pytest.mark.parametrize("initial_vector, surface_normal, expected_vector", reflect_data)
def test_reflect(initial_vector, surface_normal, expected_vector):
    assert initial_vector.reflect(surface_normal).isclose(expected_vector)


@given(initial=vectors(), normal=units())
def test_reflect_prop(initial: Vector2, normal: Vector2):
    assume(initial ^ normal != 0)
    reflected = initial.reflect(normal)
    returned = reflected.reflect(normal)
    note(f"|normal|: {normal.length}, |initial|: {initial.length}")
    note(f"angle(normal, initial): {normal.angle(initial)}")
    note(f"angle(normal, reflected): {normal.angle(reflected)}")
    note(f"initial ^ normal: {initial ^ normal}")
    note(f"Reflected: {reflected}")
    assert not any(map(isinf, reflected))
    assert initial.isclose(returned)
    note(f"initial ⋅ normal: {initial * normal}")
    note(f"reflected ⋅ normal: {reflected * normal}")
    assert isclose((initial * normal), -(reflected * normal))
    assert angle_isclose(normal.angle(initial),
                         180 - normal.angle(reflected)
    )
