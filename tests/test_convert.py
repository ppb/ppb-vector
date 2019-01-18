import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector2
from utils import vector_likes, vectors

class V(Vector2): pass

@pytest.mark.parametrize('vector_like', vector_likes(), ids=lambda x: type(x).__name__) # type: ignore
@pytest.mark.parametrize('cls', [Vector2, V]) # type: ignore
def test_convert_class(cls, vector_like):
    vector = cls.convert(vector_like)
    assert isinstance(vector, cls)
    assert vector == vector_like


@given(vector=vectors())
def test_convert_tuple(vector: Vector2):
    assert vector == tuple(vector) == (vector.x, vector.y)

@given(vector=vectors())
def test_convert_list(vector: Vector2):
    assert vector == list(vector) == [vector.x, vector.y]

@given(vector=vectors())
def test_convert_dict(vector: Vector2):
    assert vector == vector.asdict()


@pytest.mark.parametrize('coerce', [tuple, list, Vector2.asdict])
@given(x=vectors())
def test_convert_roundtrip(coerce, x: Vector2):
    assert x == Vector2(coerce(x))


@pytest.mark.parametrize('coerce', [tuple, list])
@given(x=vectors())
def test_convert_roundtrip_positional(coerce, x: Vector2):
    assert x == Vector2(*coerce(x))
