from hypothesis import given

from ppb_vector import Vector2
from utils import vectors

@given(vector=vectors())
def test_negation_coordinates(vector: Vector2):
    assert - vector.x == (- vector).x
    assert - vector.y == (- vector).y
