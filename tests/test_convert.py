import pytest  # type: ignore

from ppb_vector import Vector2
from utils import vector_likes

class V(Vector2): pass

@pytest.mark.parametrize('vector_like', vector_likes(), ids=lambda x: type(x).__name__) # type: ignore
@pytest.mark.parametrize('cls', [Vector2, V]) # type: ignore
def test_convert_class(cls, vector_like):
    vector = cls.convert(vector_like)
    assert isinstance(vector, cls)
    assert vector == vector_like
