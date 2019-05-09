from hypothesis import given

from ppb_vector import Vector
from utils import floats, vectors


@given(x=floats(), y=floats())
def test_class_member_access(x: float, y: float):
    v = Vector(x, y)
    assert v.x == x
    assert v.y == y


@given(v=vectors())
def test_index_access(v: Vector):
    assert v[0] == v.x
    assert v[1] == v.y


@given(v=vectors())
def test_key_access(v: Vector):
    assert v["x"] == v.x
    assert v["y"] == v.y
