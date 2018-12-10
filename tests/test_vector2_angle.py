from ppb_vector import Vector2
from math import isclose
import pytest  # type: ignore
from hypothesis import assume, given, note
from utils import angle_isclose, floats, vectors


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
    """Vector2.angle produces values in [-180; 180] and is antisymmetric.

    Antisymmetry means that left.angle(right) == - right.angle(left).
    """
    lr = left.angle(right)
    rl = right.angle(left)
    assert -180 < lr <= 180
    assert -180 < rl <= 180
    assert angle_isclose(lr, -rl)

@given(
    left=vectors(),
    middle=vectors(),
    right=vectors(),
)
def test_angle_additive(left, middle, right):
    """left.angle(middle) + middle.angle(right) == left.angle(right)"""
    lm = left.angle(middle)
    mr = middle.angle(right)
    lr = left.angle(right)
    assert angle_isclose(lm + mr, lr)

@given(x=vectors(), l=floats())
def test_angle_aligned(x: Vector2, l: float):
    """x.angle(l * x) is 0 or 180, depending on whether l > 0"""
    assume(l != 0)
    y = l * x
    assert angle_isclose(x.angle(y), 0 if l > 0 else 180)
