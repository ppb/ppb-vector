from hypothesis import given

from ppb_vector import Vector
from utils import vectors


@given(v=vectors())
def test_negation_scalar(v: Vector):
    assert -v == (-1) * v


@given(v=vectors())
def test_negation_involutive(v: Vector):
    assert v == -(-v)


@given(v=vectors())
def test_negation_addition(v: Vector):
    assert not (v + (-v))
