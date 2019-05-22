from hypothesis import given

from ppb_vector import Vector
from utils import vectors


@given(vector=vectors())
def test_negation_scalar(vector: Vector):
    assert -vector == (-1) * vector


@given(vector=vectors())
def test_negation_involutive(vector: Vector):
    assert vector == -(-vector)


@given(vector=vectors())
def test_negation_addition(vector: Vector):
    assert vector + (-vector) == (0, 0)
