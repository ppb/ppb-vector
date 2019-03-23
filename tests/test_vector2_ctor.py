import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector2
from utils import floats, vector_likes, vectors


class V(Vector2):
    pass


@pytest.mark.parametrize("cls", [Vector2, V])
@pytest.mark.parametrize("coerce", [tuple, list])
@given(v=vectors())
def test_ctor_roundtrip(cls, coerce, v: Vector2):
    w = cls(*coerce(v))

    assert v == w
    assert isinstance(w, cls)


@pytest.mark.parametrize("cls", [Vector2, V])
@given(x=vectors())
def test_ctor_vector_like(cls, x: Vector2):
    for x_like in vector_likes(x):
        vector = cls(x_like)
        assert vector == x == x_like
        assert isinstance(vector, cls)


@pytest.mark.parametrize("cls", [Vector2, V])
@given(x=floats(), y=floats())
def test_ctor_coordinates(cls, x: float, y: float):
    assert cls(x, y) == cls((x, y))
