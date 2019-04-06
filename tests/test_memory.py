import sys
import weakref

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector2
from utils import floats, vectors


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


@given(v=vectors())
def test_weak_ref(v):
    """Check that weak references can be made to Vector2s."""
    assert weakref.ref(v) is not None
