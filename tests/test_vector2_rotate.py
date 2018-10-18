from ppb_vector import Vector2
from utils import angle_isclose
from hypothesis import given, strategies as st
import pytest
import math

data = [
    (Vector2(1, 1), 90, Vector2(-1, 1)),
    (Vector2(1, 1), 180, Vector2(-1, -1)),
    (Vector2(1, 1), 360, Vector2(1, 1)),
    (Vector2(3, -20), 53, Vector2(17.77816, -9.64039)),
    (Vector2(math.pi, -1 * math.e), 30, Vector2(4.07984, -0.7833)),
    (Vector2(math.pi, math.e), 67, Vector2(-1.27467, 3.95397))
]

@pytest.mark.parametrize('input, degrees, expected', data)
def test_multiple_rotations(input, degrees, expected):
    assert input.rotate(degrees).isclose(expected)
    assert angle_isclose(input.angle(expected), degrees)


def test_for_exception():
    with pytest.raises(TypeError):
        Vector2('gibberish', 1).rotate(180)


@given(degree=st.floats(min_value=-360, max_value=360))
def test_trig_stability(degree):
    r = math.radians(degree)
    r_cos = math.cos(r)
    r_sin = math.sin(r)
    # Don't use exponents here. Multiplication is generally more stable.
    assert math.isclose(r_cos * r_cos + r_sin * r_sin, 1)
