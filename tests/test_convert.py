import pytest  # type: ignore

from ppb_vector import Vector2
from utils import vector_likes

@pytest.mark.parametrize('vector_like', vector_likes(), ids=lambda x: type(x).__name__) # type: ignore
def test_convert_subclass(vector_like):
    class V(Vector2): pass

    vector = V.convert(vector_like)
    assert isinstance(vector, V)
    assert vector == vector_like
