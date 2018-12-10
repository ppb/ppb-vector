from ppb_vector import Vector2
from math import isclose
import pytest  # type: ignore
from hypothesis import assume, given, note
from utils import angle_isclose, vectors


@pytest.mark.parametrize("left, right, expected", [
    (Vector2(1, 1), Vector2(0, -1), -135),
    (Vector2(1, 1), Vector2(-1, 0), 135),
    (Vector2(0, 1), Vector2(0, -1), 180),
    (Vector2(-1, -1), Vector2(1, 0), 135),
    (Vector2(-1, -1), Vector2(-1, 0), -45),
    (Vector2(1, 0), Vector2(0, 1), 90),
    (Vector2(1, 0), Vector2(1, 0), 0),
])
def test_angle(left, right, expected):
    lr = left.angle(right)
    rl = right.angle(left)
    assert -180 < lr <= 180
    assert -180 < rl <= 180
    assert isclose(lr, expected)
    assert isclose(rl, 180 if expected == 180 else -expected)


@given(
    left=vectors(),
    right=vectors(),
)
def test_angle_range(left, right):
    lr = left.angle(right)
    rl = right.angle(left)
    assert -180 < lr <= 180
    assert -180 < rl <= 180
    assert angle_isclose(lr, -rl)
