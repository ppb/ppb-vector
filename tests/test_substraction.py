import pytest  # type: ignore

from ppb_vector import Vector


def test_substraction_vectors():
    test_vector1 = Vector(0, 1)
    test_vector2 = Vector(0, 1)
    result = test_vector1 - test_vector2
    assert result == Vector(0, 0)


def test_substraction_vector_tuple():
    test_vector = Vector(4, 6)
    test_tuple = (1, 1)
    result = test_vector - test_tuple
    assert result == Vector(3, 5)


def test_substraction_vector_list():
    test_vector = Vector(3, 7)
    test_list = [1, 3]
    result = test_vector - test_list
    assert result == Vector(2, 4)


def test_substraction_vector_dict():
    test_vector = Vector(7, 11)
    test_dict = {"x": 3, "y": 5}
    result = test_vector - test_dict
    assert result == Vector(4, 6)


data = [
    ([Vector(10, 16), Vector(2, 2)], Vector(8, 14)),
    ([Vector(25, 22), Vector(22, 61)], Vector(3, -39)),
    ([Vector(39, 43), Vector(92, -12)], Vector(-53, 55)),
    ([Vector(1, 1), (2, 2)], Vector(-1, -1)),
    ([Vector(25, 22), (12, 92)], Vector(13, -70)),
    ([Vector(42, 12), (-5, 23)], Vector(47, -11)),
    ([Vector(51, 28), [72, 31]], Vector(-21, -3)),
    ([Vector(1, 2), [2, 2]], Vector(-1, 0)),
    ([Vector(1, 2), {"x": 2, "y": 2}], Vector(-1, 0)),
]


@pytest.mark.parametrize("test_input, expected", data)
def test_multiples_values(test_input, expected):
    assert (test_input[0] - test_input[1]) == expected
