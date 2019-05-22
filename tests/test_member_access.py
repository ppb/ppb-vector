import pytest  # type: ignore

from ppb_vector import Vector


@pytest.fixture()
def vector():
    return Vector(10, 20)


def test_class_member_access(vector):
    assert vector.x == 10
    assert vector.y == 20


def test_index_access(vector):
    assert vector[0] == 10
    assert vector[1] == 20


def test_key_access(vector):
    assert vector["x"] == 10
    assert vector["y"] == 20
