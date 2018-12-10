from ppb_vector import Vector2
from utils import angle_isclose, angles, floats, vectors
import pytest  # type: ignore
import math
from hypothesis import assume, given, note, example
import hypothesis.strategies as st


data_exact = [
    (Vector2(1, 1), -90, Vector2(1, -1)),
    (Vector2(1, 1),   0, Vector2(1, 1)),
    (Vector2(1, 1),  90, Vector2(-1, 1)),
    (Vector2(1, 1), 180, Vector2(-1, -1)),
]

data_close = [
    (Vector2(3, -20), 53, Vector2(17.77816, -9.64039)),
    (Vector2(math.pi, -1 * math.e), 30, Vector2(4.07984, -0.7833)),
    (Vector2(math.pi, math.e), 67, Vector2(-1.27467, 3.95397)),

    (Vector2(1, 0),  30, Vector2(math.sqrt(3)/2, 0.5)),
    (Vector2(1, 0),  60, Vector2(0.5, math.sqrt(3)/2)),
]

@pytest.mark.parametrize('input, angle, expected', data_exact)
def test_exact_rotations(input, angle, expected):
    assert input.rotate(angle) == expected
    assert input.angle(expected) == angle

@pytest.mark.parametrize('input, angle, expected', data_close)
def test_close_rotations(input, angle, expected):
    assert input.rotate(angle).isclose(expected)
    assert angle_isclose(input.angle(expected), angle)

def test_for_exception():
    with pytest.raises(TypeError):
        Vector2('gibberish', 1).rotate(180)


@given(angle=angles())
def test_trig_stability(angle):
    """cos² + sin² == 1

    We are testing that this equation holds, as otherwise rotations
    would (slightly) change the length of vectors they are applied to.
    """
    r = math.radians(angle)
    r_cos, r_sin = Vector2._trig(angle)

    # Don't use exponents here. Multiplication is generally more stable.
    assert math.isclose(r_cos * r_cos + r_sin * r_sin, 1, rel_tol=1e-18)


@given(initial=vectors(), angle=angles())
def test_rotation_angle(initial, angle):
    """initial.angle( initial.rotate(angle) ) == angle"""
    assume(initial.length > 1e-5)
    rotated = initial.rotate(angle)
    note(f"Rotated: {rotated}")

    measured_angle = initial.angle(rotated)
    d = measured_angle - angle % 360
    note(f"Angle: {measured_angle} = {angle} + {d if d<180 else d-360}")
    assert angle_isclose(angle, measured_angle)


@given(angle=angles(), loops=st.integers(min_value=0, max_value=500))
def test_rotation_stability(angle, loops):
    """Rotating loops times by angle is equivalent to rotating by loops*angle."""
    initial = Vector2(1, 0)

    fellswoop = initial.rotate(angle * loops)
    note(f"One Fell Swoop: {fellswoop}")

    stepwise = initial
    for _ in range(loops):
        stepwise = stepwise.rotate(angle)
    note(f"Step-wise: {stepwise}")

    assert fellswoop.isclose(stepwise)
    assert math.isclose(fellswoop.length, initial.length, rel_tol=1e-15)


@given(
    initial=vectors(),
    angles=st.lists(angles()),
)
def test_rotation_stability2(initial, angles):
    """Rotating by a sequence of angles is equivalent to rotating by the total."""
    total_angle = sum(angles)
    fellswoop = initial.rotate(total_angle)
    note(f"One Fell Swoop: {fellswoop}")

    stepwise = initial
    for angle in angles:
        stepwise = stepwise.rotate(angle)
    note(f"Step-wise: {stepwise}")

    assert fellswoop.isclose(stepwise)
    assert math.isclose(fellswoop.length, initial.length, rel_tol=1e-15)


@given(
    x=vectors(), y=vectors(),
    l=floats(),
    angle=angles(),
)
# In this example:
# * x * l == -y
# * Rotation must not be an multiple of 90deg
# * Must be sufficiently large
@example(
    x=Vector2(1e10, 1e10),
    y=Vector2(1e19, 1e19),
    l=-1e9,
    angle=45,
)
def test_rotation_linearity(x, y, l, angle):
    """(l*x + y).rotate is equivalent to l*x.rotate + y.rotate"""
    inner = (l * x + y).rotate(angle)
    outer = l * x.rotate(angle) + y.rotate(angle)
    note(f"l * x + y: {l * x + y}")
    note(f"l * x.rotate(): {l * x.rotate(angle)}")
    note(f"y.rotate(): {y.rotate(angle)}")
    note(f"Inner: {inner}")
    note(f"Outer: {outer}")
    assert inner.isclose(outer, rel_to=[x, l * x, y])
