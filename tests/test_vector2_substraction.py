import pytest  # type: ignore
from ppb_vector import Vector2


def test_substraction_vectors():
    test_vector1 = Vector2(0, 1)
    test_vector2 = Vector2(0, 1)
    result = test_vector1 - test_vector2
    assert result == Vector2(0, 0)


def test_substraction_vector_tuple():
    test_vector = Vector2(4, 6)
    test_tuple = (1, 1)
    result = test_vector - test_tuple
    assert result == Vector2(3, 5)


def test_substraction_vector_list():
    test_vector = Vector2(3, 7)
    test_list = [1, 3]
    result = test_vector - test_list
    assert result == Vector2(2, 4)


def test_substraction_vector_dict():
    test_vector = Vector2(7, 11)
    test_dict = {"x": 3, "y": 5}
    result = test_vector - test_dict
    assert result == Vector2(4, 6)


data = [
    ([Vector2(10, 16), Vector2(2, 2)], Vector2(8, 14)),
    ([Vector2(25, 22), Vector2(22, 61)], Vector2(3, -39)),
    ([Vector2(39, 43), Vector2(92, -12)], Vector2(-53, 55)),
    ([Vector2(1, 1), (2, 2)], Vector2(-1, -1)),
    ([Vector2(25, 22), (12, 92)], Vector2(13, -70)),
    ([Vector2(42, 12), (-5, 23)], Vector2(47, -11)),
    ([Vector2(51, 28), [72, 31]], Vector2(-21, -3)),
    ([Vector2(1, 2), [2, 2]], Vector2(-1, 0)),
    ([Vector2(1, 2), {"x": 2, "y": 2}], Vector2(-1, 0)),
]


@pytest.mark.parametrize("test_input, expected", data)
def test_multiples_values(test_input, expected):
    assert (test_input[0] - test_input[1]) == expected
