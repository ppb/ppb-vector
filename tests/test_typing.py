import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import *


@pytest.mark.parametrize("op", BINARY_OPS | BINARY_SCALAR_OPS | BOOL_OPS)  # type: ignore
@given(x=vectors(), y=units())
def test_binop_vectorlike(op, x: Vector, y: Vector):
    """Test that `op` accepts a vector-like second parameter."""
    result = op(x, y)

    for y_like in vector_likes(y):
        assert op(x, y_like) == result
