import pytest
from ppb_vector import Vector2


@pytest.fixture()
def test_vector():
    return Vector2(10, 20)


def test_vector_2_class_member_access(test_vector):
    assert test_vector.x == 10
    assert test_vector.y == 20


def test_vector2_index_access(test_vector):
    assert test_vector[0] == 10
    assert test_vector[1] == 20


def test_vector2_key_access(test_vector):
    assert test_vector['x'] == 10
    assert test_vector['y'] == 20
