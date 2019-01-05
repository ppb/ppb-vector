from hypothesis import given

from ppb_vector import Vector2
from utils import vectors

@given(vector=vectors())
def test_negation_scalar(vector: Vector2):
    assert - vector == (-1) * vector
