from hypothesis import given
from ppb_vector import Vector2
from utils import vectors

def test_equal():
  test_vector_1 = Vector2(50, 800)
  test_vector_2 = Vector2(50, 800)

  assert test_vector_1 == test_vector_2


@given(x=vectors(), y=vectors())
def test_not_equal_equivalent(x: Vector2, y: Vector2):
  assert (x != y) == (not x == y)
