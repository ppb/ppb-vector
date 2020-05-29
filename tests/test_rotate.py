import math
from math import cos, fabs, radians, sin, sqrt

import hypothesis.strategies as st
import pytest  # type: ignore
from hypothesis import assume, example, given, note

from ppb_vector import Vector
from utils import angle_isclose, angles, floats, isclose, vectors


data_exact = [
    (Vector(1, 1), -90, Vector(1, -1)),
    (Vector(1, 1), 0, Vector(1, 1)),
    (Vector(1, 1), 90, Vector(-1, 1)),
    (Vector(1, 1), 180, Vector(-1, -1)),
]


@pytest.mark.parametrize("input, angle, expected", data_exact,
                         ids=[str(angle) for _, angle, _ in data_exact])
def test_exact_rotations(input, angle, expected):
    assert input.rotate(angle) == expected
    assert input.angle(expected) == angle


# angle (in degrees) -> (sin, cos)
#  values from 0 to 45°
#  lifted from https://en.wikibooks.org/wiki/Trigonometry/Selected_Angles_Reference
remarkable_angles = {
    15: ((sqrt(6) + sqrt(2)) / 4, (sqrt(6) - sqrt(2)) / 4),
    22.5: (sqrt(2 + sqrt(2)) / 2, sqrt(2 - sqrt(2)) / 2),
    30: (sqrt(3) / 2, 0.5),
    45: (sqrt(2) / 2, sqrt(2) / 2),
}

#  extend up to 90°
remarkable_angles.update({
    90 - angle: (sin_t, cos_t)
    for angle, (cos_t, sin_t) in remarkable_angles.items()
})

#  extend up to 180°
remarkable_angles.update({
    angle + 90: (-sin_t, cos_t)
    for angle, (cos_t, sin_t) in remarkable_angles.items()
})

#  extend up to 360°
remarkable_angles.update({
    angle + 180: (-cos_t, -sin_t)
    for angle, (cos_t, sin_t) in remarkable_angles.items()
})

#  extend to negative angles
remarkable_angles.update({
    -angle: (cos_t, -sin_t)
    for angle, (cos_t, sin_t) in remarkable_angles.items()
})


@pytest.mark.parametrize("angle, trig", remarkable_angles.items(),
                         ids=[str(x) for x in remarkable_angles])
def test_remarkable_angles(angle, trig):
    """Test that our table of remarkable angles agrees with Vector._trig.

    This is useful both as a consistency test of the table,
    and as a test of Vector._trig (which Vector.rotate uses).
    """
    cos_t, sin_t = trig
    cos_m, sin_m = Vector._trig(angle)

    assert isclose(sin_t, sin_m, abs_tol=0, rel_tol=1e-14)
    assert isclose(cos_t, cos_m, abs_tol=0, rel_tol=1e-14)


data_close = [
    (Vector(1, 0), angle, Vector(cos_t, sin_t))
    for (angle, (cos_t, sin_t)) in remarkable_angles.items()
] + [
    (Vector(1, 1), angle, Vector(cos_t - sin_t, cos_t + sin_t))
    for (angle, (cos_t, sin_t)) in remarkable_angles.items()
]


@pytest.mark.parametrize("input, angle, expected", data_close,
                         ids=[f"({v.x},{v.y}).rotate({angle})" for v, angle, _ in data_close])
def test_close_rotations(input, angle, expected):
    assert input.rotate(angle).isclose(expected)
    assert angle_isclose(input.angle(expected), angle)


@given(angle=angles())
def test_trig_stability(angle):
    """cos² + sin² == 1

    We are testing that this equation holds, as otherwise rotations
    would (slightly) change the length of vectors they are applied to.

    Moreover, Vector._trig should get closer to fulfilling it than
    math.{cos,sin}.
    """
    r_cos, r_sin = Vector._trig(angle)
    r_len = r_cos * r_cos + r_sin * r_sin

    # Don't use exponents here. Multiplication is generally more stable.
    assert math.isclose(r_len, 1, rel_tol=1e-18)

    t_cos, t_sin = cos(radians(angle)), sin(radians(angle))
    t_len = t_cos * t_cos + t_sin * t_sin
    assert fabs(1 - r_len) <= fabs(1 - t_len)


@given(angle=angles(), n=st.integers(min_value=0, max_value=100_000))
def test_trig_invariance(angle: float, n: int):
    """Test that cos(θ), sin(θ) ≃ cos(θ + n*360°), sin(θ + n*360°)"""
    r_cos, r_sin = Vector._trig(angle)
    n_cos, n_sin = Vector._trig(angle + 360 * n)

    note(f"δcos: {r_cos - n_cos}")
    assert isclose(r_cos, n_cos, rel_to=[n / 1e9])
    note(f"δsin: {r_sin - n_sin}")
    assert isclose(r_sin, n_sin, rel_to=[n / 1e9])


@given(v=vectors(), angle=angles(), n=st.integers(min_value=0, max_value=100_000))
def test_rotation_invariance(v: Vector, angle: float, n: int):
    """Check that rotating by angle and angle + n×360° have the same result."""
    rot_once = v.rotate(angle)
    rot_many = v.rotate(angle + 360 * n)
    note(f"δ: {(rot_once - rot_many).length}")
    assert rot_once.isclose(rot_many, rel_tol=n / 1e9)


@given(initial=vectors(), angle=angles())
def test_rotation_angle(initial, angle):
    """initial.angle( initial.rotate(angle) ) == angle"""
    assume(initial.length > 1e-5)
    assert angle_isclose(initial.angle(initial.rotate(angle)), angle)


@given(angle=angles(), loops=st.integers(min_value=0, max_value=500))
def test_rotation_stability(angle, loops):
    """Rotating loops times by angle is equivalent to rotating by loops*angle."""
    initial = Vector(1, 0)

    fellswoop = initial.rotate(angle * loops)
    note(f"One Fell Swoop: {fellswoop}")

    stepwise = initial
    for _ in range(loops):
        stepwise = stepwise.rotate(angle)
    note(f"Step-wise: {stepwise}")

    assert fellswoop.isclose(stepwise, rel_tol=1e-8)
    assert math.isclose(fellswoop.length, initial.length, rel_tol=1e-15)


@given(initial=vectors(), angles=st.lists(angles()))
def test_rotation_stability2(initial, angles):
    """Rotating by a sequence of angles is equivalent to rotating by the total."""
    total_angle = sum(angles)
    fellswoop = initial.rotate(total_angle)
    note(f"One Fell Swoop: {fellswoop}")

    stepwise = initial
    for angle in angles:
        stepwise = stepwise.rotate(angle)
    note(f"Step-wise: {stepwise}")

    # Increase the tolerance on this comparison,
    # as stepwise rotations induce rounding errors
    assert fellswoop.isclose(stepwise, rel_tol=1e-6)
    assert math.isclose(fellswoop.length, initial.length, rel_tol=1e-15)


@given(x=vectors(), y=vectors(), scalar=floats(), angle=angles())
# In this example:
# * x * l == -y
# * Rotation must not be an multiple of 90deg
# * Must be sufficiently large
@example(x=Vector(1e10, 1e10), y=Vector(1e19, 1e19), scalar=-1e9, angle=45)
def test_rotation_linearity(x, y, scalar, angle):
    """(l*x + y).rotate is equivalent to l*x.rotate + y.rotate"""
    inner = (scalar * x + y).rotate(angle)
    outer = scalar * x.rotate(angle) + y.rotate(angle)
    note(f"scalar * x + y: {scalar * x + y}")
    note(f"scalar * x.rotate(): {scalar * x.rotate(angle)}")
    note(f"y.rotate(): {y.rotate(angle)}")
    note(f"Inner: {inner}")
    note(f"Outer: {outer}")
    assert inner.isclose(outer, rel_to=[x, scalar * x, y])
