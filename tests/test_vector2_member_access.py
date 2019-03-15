import pytest  # type: ignore

from ppb_vector import Vector2


@pytest.fixture()
def vector():
    return Vector2(10, 20)


def test_vector2_class_member_access(vector):
    assert vector.x == 10
    assert vector.y == 20


def test_vector2_index_access(vector):
    assert vector[0] == 10
    assert vector[1] == 20


def test_vector2_key_access(vector):
    assert vector["x"] == 10
    assert vector["y"] == 20
