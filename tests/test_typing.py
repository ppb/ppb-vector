import pytest

from ppb_vector import Vector2

# List of operations that (Vector2, Vector2) -> Vector2
BINARY_OPS = [
    Vector2.__add__,
    Vector2.__sub__,
    Vector2.reflect,
]

# List of operations that (Vector2, Real) -> Vector2
VECTOR_NUMBER_OPS = [
    Vector2.__mul__,
    Vector2.__rmul__,
    Vector2.rotate,
    Vector2.truncate,
    Vector2.scale,
]

# List of operations that (Vector2) -> Vector2
UNARY_OPS = [
    Vector2.convert,
    Vector2.__neg__,
    Vector2.normalize,
]

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


@pytest.mark.parametrize('op', VECTOR_NUMBER_OPS)
def test_vnumop(op):
    class V(Vector2): pass
    
    a = op(V(1, 2), 42)

    assert isinstance(a, V)


@pytest.mark.parametrize('op', UNARY_OPS)
def test_monop(op):
    class V(Vector2): pass
    
    a = op(V(1, 2))

    assert isinstance(a, V)
