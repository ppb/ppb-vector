import pickle

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import floats, vector_likes, vectors


@given(x=vectors())
def test_ctor_vector_like(x: Vector):
    for x_like in vector_likes(x):
        vector = Vector(x_like)
        assert vector == x == x_like
        assert isinstance(vector, cls)


@given(x=floats(), y=floats())
def test_ctor_coordinates(x: float, y: float):
    assert Vector(x, y) == Vector((x, y))


def test_ctor_noncopy_same():
    v = Vector(1, 2)
    assert Vector(v) is v


@given(v=vectors())
def test_ctor_pickle(v: Vector):
    """Round-trip Vector and subclasses through `pickle.{dumps,loads}`."""
    w = pickle.loads(pickle.dumps(v))

    assert v == w
    assert isinstance(w, Vector)
