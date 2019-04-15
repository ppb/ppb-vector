from dataclasses import dataclass

import pytest  # type: ignore
from hypothesis import assume, given, strategies as st

from ppb_vector import Vector2
from utils import *


@dataclass(frozen=True, init=False)
class LabeledVector(Vector2):
    """Subclass of Vector2 that defines an additional attribute."""
    label: str

    def __init__(self, x, y, label):
        Vector2.__init__(self, x, y)
        object.__setattr__(self, 'label', label)


@given(v=vectors(), label_v=st.text())
def test_subclass_copy(v: Vector2, label_v: str):
    """Test that instances of the subclass can be copied."""
    from copy import copy, deepcopy
    v = LabeledVector(*v, label_v)  # type: ignore
    w = copy(v)

    assert v == w == deepcopy(v)
    assert w.label == label_v


@given(v=vectors(), label_v=st.text())
def test_ctor_pickle(v: Vector2, label_v: str):
    """Round-trip instances of the subclass through `pickle.{dumps,loads}`."""
    import pickle
    v = LabeledVector(*v, label_v)  # type: ignore
    w = pickle.loads(pickle.dumps(v))

    assert v == w
    assert isinstance(w, LabeledVector)


@pytest.mark.parametrize("op", BINARY_OPS)
@given(v=vectors(), label_v=st.text(), w=units(), label_w=st.text())
def test_subclass_binops_both(op, v: Vector2, label_v: str, w: Vector2, label_w: str):
    """Test that binary operators preserve attributes when applied to another LabelledVector."""
    v = LabeledVector(*v, label_v)  # type: ignore
    w = LabeledVector(*w, label_w)  # type: ignore
    u = op(v, w)

    assert isinstance(u, LabeledVector)
    assert u.label == label_v


@pytest.mark.parametrize("op", BINARY_OPS)
@given(v=vectors(), label=st.text(), w=units())
def test_subclass_binops_one(op, v: Vector2, label: str, w: Vector2):
    """Test that binary operators preserve extra attributes when applied to a Vector2."""
    v = LabeledVector(*v, label)  # type: ignore
    u = op(v, w)

    assert isinstance(u, LabeledVector)
    assert u.label == label


@pytest.mark.parametrize("op", SCALAR_OPS)
@given(v=vectors(), label=st.text(), scalar=lengths())
def test_subclass_scalar(op, v: Vector2, label: str, scalar: float):
    """Test that scalar operators preserve extra attributes."""
    assume(scalar != 0 and v.length != 0)
    v = LabeledVector(*v, label)  # type: ignore
    u = op(v, scalar)

    assert isinstance(u, LabeledVector)
    assert u.label == label


@pytest.mark.parametrize("op", UNARY_OPS - set([Vector2]))
@given(v=vectors(), label=st.text())
def test_subclass_unary(op, v: Vector2, label: str):
    """Test that unary operators preserve extra attributes."""
    assume(v.length != 0)
    v = LabeledVector(*v, label)  # type: ignore
    u = op(v)

    assert isinstance(u, LabeledVector)
    assert u.label == label
