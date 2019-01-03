import pytest  # type: ignore
from hypothesis import event, given, reject, strategies as st

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
@given(x=st.builds(V1, vectors()), y=st.builds(V1, units()))
def test_binop_same(op, x: V1, y: V2):
    assert isinstance(op(x, y), V1)


@pytest.mark.parametrize('op', BINARY_OPS)
@given(x=vectors(), y=units())
def test_binop_different(op, x: Vector2, y: Vector2):
    assert isinstance(op(V1(x), V2(y)), (V1, V2))
    assert isinstance(op(V2(x), V1(y)), (V1, V2))


@pytest.mark.parametrize('op', BINARY_OPS)
@given(x=st.builds(V1, vectors()), y=st.builds(V1, units()))
def test_binop_subclass(op, x: V1, y: V1):
    assert isinstance(op(V11(x), y), V11)
    assert isinstance(op(x, V11(y)), V11)


@pytest.mark.parametrize('op', SCALAR_OPS)
@given(x=st.builds(V1, vectors()), scalar=floats())
def test_vnumop(op, x: V1, scalar: float):
    try:
        assert isinstance(op(x, scalar), V1)
    except (ValueError, ZeroDivisionError) as e:
        event(type(e).__name__)
        reject()


@pytest.mark.parametrize('op', UNARY_OPS)
@given(x=st.builds(V1, vectors()))
def test_monop(op, x):
    try:
        assert isinstance(op(x), V1)
    except (ValueError, ZeroDivisionError) as e:
        event(type(e).__name__)
        reject()


@pytest.mark.parametrize('op', BINARY_OPS + BINARY_SCALAR_OPS + BOOL_OPS) # type: ignore
@given(x=vectors(), y=units())
def test_binop_vectorlike(op, x: Vector2, y: Vector2):
    """Test that `op` accepts a vector-like second parameter."""
    result = op(x, y)

    for y_like in vector_likes(y):
        assert op(x, y_like) == result
