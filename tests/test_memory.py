import sys
import weakref
from dataclasses import dataclass

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector2
from test_subclass import LabeledVector
from utils import floats, vectors


@given(v=vectors())
def test_weak_ref(v):
    """Check that weak references can be made to Vector2s."""
    assert weakref.ref(v) is not None


class DummyVector:
    """A naïve representation of vectors."""

    x: float
    y: float

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


@pytest.mark.skipif(sys.implementation.name != 'cpython',
                    reason="PyPy optimises __slots__ automatically.")
@given(x=floats(), y=floats())
def test_object_size(x, y):
    """Check that Vector2 is 2 times smaller than a naïve version."""
    from pympler.asizeof import asizeof as sizeof  # type: ignore

    assert sizeof(Vector2(x, y)) < sizeof(DummyVector(x, y)) / 2


@dataclass(frozen=True, init=False)
class SlottedVector(Vector2):
    """Subclass of Vector2 that defines an additional attribute & its slot."""
    label: str
    __slots__ = ('label',)

    def __new__(cls, x, y, label):
        self = super().__new__(cls, x, y)
        object.__setattr__(self, 'label', label)
        return self


@pytest.mark.skipif(sys.implementation.name != 'cpython',
                    reason="PyPy optimises __slots__ automatically.")
@given(v=vectors())
def test_subclass_size(v):
    """Check that the slots optimization works on subclasses."""
    from pympler.asizeof import asizeof as sizeof  # type: ignore
    assert sizeof(v) < sizeof(SlottedVector(*v, None)) < sizeof(LabeledVector(*v, None)) / 2
