from hypothesis import assume, given
from ppb_vector import Vector2
from utils import vectors


@given(x=vectors())
def test_equal_self(x: Vector2):
  assert x == x

@given(x=vectors())
def test_non_zero_equal(x: Vector2):
  assume(x != (0, 0))
  assert x != 1.1 * x
  assert x != -x

@given(x=vectors(), y=vectors())
def test_not_equal_equivalent(x: Vector2, y: Vector2):
  assert (x != y) == (not x == y)
