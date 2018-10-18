from ppb_vector import Vector2
from hypothesis import given, note, strategies as st
from math import isclose
from numbers import Real
from utils import vectors
import pytest  # type: ignore

@pytest.mark.parametrize("left, right, expected", [
    (Vector2(1, 1), Vector2(0, -1), -1),
    (Vector2(1, 1), Vector2(-1, 0), 1),
    (Vector2(0, 1), Vector2(0, -1), 0),
    (Vector2(-1, -1), Vector2(1, 0), 1),
    (Vector2(-1, -1), Vector2(-1, 0), -1)
])
def test_cross(left, right, expected):
    assert left ^ right == expected
    assert right ^ left == -expected


@given(a=vectors(max_magnitude=1e150), c=vectors(max_magnitude=1e150),
       b=vectors(max_magnitude=1e75),
       l=st.floats(min_value=-1e75,max_value=1e75),
)
def test_cross_linearity(a: Vector2, b: Vector2, c: Vector2, l: Real):
    factored = a ^ (l * b + c)
    distributed = l * (a^b) + (a^c)

    note(f"a ^ (l * b + c): {factored}")
    note(f"l * (a^b) + (a^c): {distributed}")
    assert isclose(factored, distributed)

@given(a=vectors(max_magnitude=1e150), b=vectors(max_magnitude=1e150))
def test_cross_antisymetry(a: Vector2, b: Vector2):
    prod1 = a ^ b
    prod2 = b ^ a

    note(f"a ^ b: {prod1}")
    note(f"b ^ a: {prod2}")
    note(f"δ: {prod1 + prod2}")
    assert isclose(prod1, -prod2)
