import pytest  # type: ignore

from ppb_vector import Vector2
from utils import *


class V1(Vector2):
    """Arbitrary subclass of Vector2."""
    pass

class V11(V1):
    """Subclass of V1."""
    pass

class V2(Vector2):
    """Arbitrary subclass of Vector2, distinct from V1."""
    pass


@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_same(op):
    # Normalize for reflect
    a = op(V1(1, 2), V1(3, 4).normalize())

    assert isinstance(a, V1)


@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_different(op):
    # Normalize for reflect
    a = op(V1(1, 2), V2(3, 4).normalize())
    b = op(V2(1, 2), V1(3, 4).normalize())
    assert isinstance(a, (V1, V2))
    assert isinstance(b, (V1, V2))


@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_subclass(op):
    # Normalize for reflect
    a = op(V1(1, 2), V11(3, 4).normalize())
    b = op(V11(1, 2), V1(3, 4).normalize())
    assert isinstance(a, V11)
    assert isinstance(b, V11)


@pytest.mark.parametrize('op', SCALAR_OPS)
def test_vnumop(op):
    a = op(V1(1, 2), 42)
    assert isinstance(a, V1)


@pytest.mark.parametrize('op', UNARY_OPS)
def test_monop(op):
    a = op(V1(1, 2))
    assert isinstance(a, V1)


@pytest.mark.parametrize('op', BINARY_OPS + BINARY_SCALAR_OPS + BOOL_OPS) # type: ignore
def test_binop_vectorlike(op):
    """Test that `op` accepts a vector-like second parameter."""
    x = Vector2(1, 0)
    y = Vector2(0, 1)
    result = op(x, y)

    for y_like in vector_likes(y):
        assert op(x, y_like) == result
