from hypothesis import assume, given

from ppb_vector import Vector
from utils import vector_likes, vectors


@given(x=vectors())
def test_equal_self(x: Vector):
    assert x == x


@given(x=vectors())
def test_equal_non_vector(x: Vector):
    assert x != "foo"
    assert (x == "foo") == ("foo" == x)


@given(x=vectors(), y=vectors())
def test_equal_symmetric(x: Vector, y):
    assert (x == y) == (y == x)

    for y_like in vector_likes(y):
        assert (x == y_like) == (y_like == x)


@given(x=vectors())
def test_non_zero_equal(x: Vector):
    assume(x)
    assert x != 1.1 * x
    assert x != -x


@given(x=vectors(), y=vectors())
def test_not_equal_equivalent(x: Vector, y: Vector):
    assert (x != y) == (not x == y)
