import pytest  # type: ignore

from ppb_vector import Vector2
from utils import *

@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_same(op):
    class V(Vector2): pass

    # Normalize for reflect
    a = op(V(1, 2), V(3, 4).normalize())

    assert isinstance(a, V)


@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_different(op):
    class V1(Vector2): pass
    class V2(Vector2): pass

    # Normalize for reflect
    a = op(V1(1, 2), V2(3, 4).normalize())
    b = op(V2(1, 2), V1(3, 4).normalize())
    assert isinstance(a, (V1, V2))
    assert isinstance(b, (V1, V2))


@pytest.mark.parametrize('op', BINARY_OPS)
def test_binop_subclass(op):
    class V1(Vector2): pass
    class V2(V1): pass

    # Normalize for reflect
    a = op(V1(1, 2), V2(3, 4).normalize())
    b = op(V2(1, 2), V1(3, 4).normalize())
    assert isinstance(a, V2)
    assert isinstance(b, V2)


@pytest.mark.parametrize('op', SCALAR_OPS)
def test_vnumop(op):
    class V(Vector2): pass

    a = op(V(1, 2), 42)

    assert isinstance(a, V)


@pytest.mark.parametrize('op', UNARY_OPS)
def test_monop(op):
    class V(Vector2): pass

    a = op(V(1, 2))

    assert isinstance(a, V)


@pytest.mark.parametrize('op', BINARY_OPS + BINARY_SCALAR_OPS + BOOL_OPS) # type: ignore
def test_binop_vectorlike(op):
    """Test that `op` accepts a vector-like second parameter."""
    x = Vector2(1, 0)
    result = op(x, Vector2(0, 1))

    for y_like in [ (0, 1), [0, 1], {"x": 0, "y": 1} ]:
        assert op(x, y_like) == result
