from dataclasses import dataclass

import pytest  # type: ignore
from hypothesis import given, strategies as st

from ppb_vector import Vector2
from utils import *


@dataclass(frozen=True, init=False)
class LabeledVector(Vector2):
    """Subclass of Vector2 that defines an additional attribute."""
    label: str

    def __new__(cls, x, y, label):
        self = super().__new__(cls, x, y)
        object.__setattr__(self, 'label', label)
        return self


@pytest.mark.parametrize("op", BINARY_OPS)
@given(v=vectors(), label_v=st.text(), w=vectors(), label_w=st.text())
def test_subclass_binops_both(op, v: Vector2, label_v: str, w: Vector2, label_w: str):
    """Test that binary operators preserve attributes when applied to another LabelledVector."""
    v = LabeledVector(*v, label_v)
    w = LabeledVector(*w, label_w)
    u = op(v, w)

    assert isinstance(u, LabeledVector)
    assert u.label == label_v


@pytest.mark.parametrize("op", BINARY_OPS)
@given(v=vectors(), label=st.text(), w=vectors())
def test_subclass_binops_one(op, v: Vector2, label: str, w: Vector2):
    """Test that binary operators preserve extra attributes when applied to a Vector2."""
    v = LabeledVector(*v, label)
    u = op(v, w)

    assert isinstance(u, LabeledVector)
    assert u.label == label


@pytest.mark.parametrize("op", SCALAR_OPS)
@given(v=vectors(), label=st.text(), scalar=floats())
def test_subclass_scalar(op, v: Vector2, label: str, scalar: float):
    """Test that scalar operators preserve extra attributes."""
    v = LabeledVector(*v, label)
    u = op(v, scalar)

    assert isinstance(u, LabeledVector)
    assert u.label == label


@pytest.mark.parametrize("op", UNARY_OPS)
@given(v=vectors(), label=st.text())
def test_subclass_unary(op, v: Vector2, label: str):
    """Test that unary operators preserve extra attributes."""
    v = LabeledVector(*v, label)
    u = op(v)

    assert isinstance(u, LabeledVector)
    assert u.label == label
