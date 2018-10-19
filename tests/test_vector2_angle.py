from ppb_vector import Vector2
from math import isclose
import pytest

@pytest.mark.parametrize("left, right, expected", [
    (Vector2(1, 1), Vector2(0, -1), -135),
    (Vector2(1, 1), Vector2(-1, 0), 135),
    (Vector2(0, 1), Vector2(0, -1), 180),
    (Vector2(-1, -1), Vector2(1, 0), 135),
    (Vector2(-1, -1), Vector2(-1, 0), 45),
    (Vector2(1, 0), Vector2(0, 1), 90),
    (Vector2(1, 0), Vector2(1, 0), 0),
])
def test_angle(left, right, expected):
    assert isclose(left.angle(right), expected)
    assert isclose(right.angle(left), expected)
