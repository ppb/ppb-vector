import pickle

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import floats, vector_likes, vectors


class V(Vector):
    pass


@pytest.mark.parametrize("cls", [Vector, V])
@given(x=vectors())
def test_ctor_vector_like(cls, x: Vector):
    for x_like in vector_likes(x):
        vector = cls(x_like)
        assert vector == x == x_like
        assert isinstance(vector, cls)


@pytest.mark.parametrize("cls", [Vector, V])
@given(x=floats(), y=floats())
def test_ctor_coordinates(cls, x: float, y: float):
    assert cls(x, y) == cls((x, y))


@pytest.mark.parametrize("cls", [Vector, V])
def test_ctor_noncopy_same(cls):
    v = cls(1, 2)
    assert cls(v) is v


def test_ctor_noncopy_subclass():
    v = V(1, 2)
    assert Vector(v) is v


def test_ctor_noncopy_superclass():
    v = Vector(1, 2)
    assert V(v) is not v


@pytest.mark.parametrize("cls", [Vector, V])
@given(v=vectors())
def test_ctor_pickle(cls, v: Vector):
    """Round-trip Vector and subclasses through `pickle.{dumps,loads}`."""
    w = pickle.loads(pickle.dumps(cls(v)))

    assert v == w
    assert isinstance(w, cls)
