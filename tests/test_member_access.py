from hypothesis import given
import pytest  # type: ignore

from ppb_vector import Vector
from utils import vectors


@pytest.fixture()
def vector():
    return Vector(10, 20)


def test_class_member_access(vector):
    assert vector.x == 10
    assert vector.y == 20


@given(v=vectors())
def test_index_access(v: Vector):
    assert v[0] == v.x
    assert v[1] == v.y


@given(v=vectors())
def test_key_access(v: Vector):
    assert v["x"] == v.x
    assert v["y"] == v.y
