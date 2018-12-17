import pytest  # type: ignore

from ppb_vector import Vector2
from utils import BINARY_OPS, SCALAR_OPS, UNARY_OPS

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
