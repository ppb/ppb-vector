from ppb_vector import Vector2
import pytest
from hypothesis import given, assume, note
import hypothesis.strategies as st
from math import isclose

reflect_data = (
    (Vector2(1, 1), Vector2(0, -1), Vector2(1, -1)),
    (Vector2(1, 1), Vector2(-1, 0), Vector2(-1, 1)),
    (Vector2(0, 1), Vector2(0, -1), Vector2(0, -1)),
    (Vector2(-1, -1), Vector2(1, 0), Vector2(1, -1)),
    (Vector2(-1, -1), Vector2(-1, 0), Vector2(-1,1))
)


@pytest.mark.parametrize("initial_vector, surface_normal, expected_vector", reflect_data)
def test_reflect(initial_vector, surface_normal, expected_vector):
    assert initial_vector.reflect(surface_normal) == expected_vector


stvector = lambda: st.builds(
    Vector2, 
    st.floats(allow_nan=False, allow_infinity=False), 
    st.floats(allow_nan=False, allow_infinity=False)
)


def isclose_vector(a, b, *, rel_tol=1e-09, abs_tol=1e-5):
    return isclose(a.x, b.x, rel_tol=rel_tol, abs_tol=abs_tol) and isclose(a.y, b.y, rel_tol=rel_tol, abs_tol=abs_tol)


@given(initial=stvector(), normal=stvector())
def test_reflect_prop(initial: Vector2, normal: Vector2):
    assume(initial != Vector2(0, 0))
    assume(normal != Vector2(0, 0))
    assume(initial ^ normal != 0)  # FIXME: cross product
    normal = normal.normalize()
    reflected = initial.reflect(normal)
    returned = reflected.reflect(normal)
    note(f"Reflected: {reflected}")
    note(f"Re-Reflected: {returned}")
    assert isclose_vector(initial, returned)
    assert isclose((initial * normal), -(reflected * normal))
