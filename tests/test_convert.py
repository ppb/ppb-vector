import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import vector_likes, vectors


@pytest.mark.parametrize(
    "vector_like", vector_likes(), ids=lambda x: type(x).__name__,
)
def test_convert_class(vector_like):
    vector = Vector(vector_like)
    assert isinstance(vector, Vector)
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
