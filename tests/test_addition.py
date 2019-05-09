import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import vector_likes, vectors


data = [
    ((1, 0),   (0, 1),    (1, 1)),
    ((1, 1),   (2, 2),    (3, 3)),
    ((1, 2),   (2, 2),    (3, 4)),
    ((10, 16), (2, 2),    (12, 18)),
    ((25, 22), (12, 92),  (37, 114)),
    ((25, 22), (22, 61),  (47, 83)),
    ((39, 43), (92, -12), (131, 31)),
    ((42, 12), (-5, 23),  (37, 35)),
    ((51, 28), (72, 31),  (123, 59)),
]


@pytest.mark.parametrize("x, y, expected", data)
def test_multiples_values(x, y, expected):
    assert (Vector(x) + y) == expected


@given(x=vectors(), y=vectors())
def test_addition_reverse(x: Vector, y: Vector):
    for y_like in vector_likes(y):
        assert y_like + x == x + y
