import weakref

from pympler.asizeof import asizeof as sizeof  # type: ignore
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


@given(x=floats(), y=floats())
def test_object_size(x, y):
    """Check that Vector2 is 3 times smaller than a naïve version."""
    assert sizeof(Vector2(x, y)) < sizeof(DummyVector(x, y)) / 3


@given(v=vectors())
def test_weak_ref(v):
    """Check that weak references can be made to Vector2s."""
    assert weakref.ref(v) is not None
