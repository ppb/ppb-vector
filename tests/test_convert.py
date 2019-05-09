import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import vector_likes, vectors


class V(Vector):
    pass


@pytest.mark.parametrize(
    "vector_like", vector_likes(), ids=lambda x: type(x).__name__,
)
@pytest.mark.parametrize("cls", [Vector, V])  # type: ignore
def test_convert_class(cls, vector_like):
    vector = cls(vector_like)
    assert isinstance(vector, cls)
    assert vector == vector_like


@given(vector=vectors())
def test_convert_tuple(vector: Vector):
    assert vector == tuple(vector) == (vector.x, vector.y)


@given(vector=vectors())
def test_convert_list(vector: Vector):
    assert vector == list(vector) == [vector.x, vector.y]


@given(vector=vectors())
def test_convert_dict(vector: Vector):
    assert vector == vector.asdict()


@pytest.mark.parametrize("coerce", [tuple, list, Vector.asdict])
@given(x=vectors())
def test_convert_roundtrip(coerce, x: Vector):
    assert x == Vector(coerce(x))


@pytest.mark.parametrize("coerce", [tuple, list])
@given(x=vectors())
def test_convert_roundtrip_positional(coerce, x: Vector):
    assert x == Vector(*coerce(x))
