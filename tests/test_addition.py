import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import vector_likes, vectors


data = [
    ([Vector(1, 0), (0, 1)], Vector(1, 1)),
    ([Vector(1, 1), (2, 2)], Vector(3, 3)),
    ([Vector(1, 2), [2, 2]], Vector(3, 4)),
    ([Vector(10, 16), Vector(2, 2)], Vector(12, 18)),
    ([Vector(25, 22), (12, 92)], Vector(37, 114)),
    ([Vector(25, 22), Vector(22, 61)], Vector(47, 83)),
    ([Vector(39, 43), Vector(92, -12)], Vector(131, 31)),
    ([Vector(42, 12), (-5, 23)], Vector(37, 35)),
    ([Vector(51, 28), [72, 31]], Vector(123, 59)),
]


@pytest.mark.parametrize("test_input, expected", data)
def test_multiples_values(test_input, expected):
    assert (test_input[0] + test_input[1]) == expected


@given(x=vectors(), y=vectors())
def test_addition_reverse(x: Vector, y: Vector):
    for y_like in vector_likes(y):
        assert y_like + x == x + y
