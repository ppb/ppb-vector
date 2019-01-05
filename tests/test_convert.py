import pytest  # type: ignore

from ppb_vector import Vector2
from utils import vector_likes

@pytest.mark.parametrize('vector_like', vector_likes()) # type: ignore
def test_convert_subclass(vector_like):
    class V(Vector2): pass

    # test_binop_vectorlike already checks the output value is correct
    assert isinstance(V.convert(vector_like), V)
