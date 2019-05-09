from math import sqrt

from hypothesis import assume, given, note
from hypothesis.strategies import floats
from pytest import raises  # type: ignore

from ppb_vector import Vector
from utils import lengths, units, vectors


@given(v=vectors(), abs_tol=floats(min_value=0), rel_tol=floats(min_value=0))
def test_isclose_to_self(v, abs_tol, rel_tol):
    assert v.isclose(v, abs_tol=abs_tol, rel_tol=rel_tol)


EPSILON = 1e-8


@given(v=vectors(max_magnitude=1e30), direction=units(), abs_tol=lengths(max_value=1e30))
def test_isclose_abs_error(v, direction, abs_tol):
    """Test v.isclose(rel_tol=0) near the boundary between “close” and “not close”

    - v + (1 - ε) * abs_tol * direction should be close
    - v + (1 + ε) * abs_tol * direction shouldn't be close
    """
    assume(abs_tol > EPSILON * v.length)
    note(f"|v|: {v.length}")

    error = abs_tol * direction
    positive = v + (1 - sqrt(EPSILON)) * error
    note(f"positive example: {positive} = v + {positive - v}")
    assert v.isclose(positive, abs_tol=abs_tol, rel_tol=0)

    negative = v + (1 + sqrt(EPSILON)) * abs_tol * direction
    note(f"negative example: {negative} = v + {negative - v}")
    assert not v.isclose(negative, abs_tol=abs_tol, rel_tol=0)


@given(
    v=vectors(max_magnitude=1e30),
    direction=units(),
    rel_tol=floats(min_value=EPSILON, max_value=1 - sqrt(EPSILON)),
)
def test_isclose_rel_error(v, direction, rel_tol):
    """Test v.isclose(abs_tol=0) near the boundary between “close” and “not close”

    - v + (1 - ε) * |v| * rel_tol * direction should always be close
    - We can also generate an example that isn't close,
      though the formula is somewhat complicated.
    """
    assume(v.length > EPSILON)
    note(f"|v| = {v.length}")
    error = rel_tol * direction

    positive = v + (1 - sqrt(EPSILON)) * v.length * error
    note(
        f"positive example: {positive} = v + {positive - v} = "
        f"v + {(positive - v).length / v.length} * |v| * direction",
    )

    assert v.isclose(positive, abs_tol=0, rel_tol=rel_tol)

    # In v.isclose(negative), the allowed relative error is relative to |v|
    # and |negative|, so the acceptable errors grow larger as negative does.
    #
    # We must account for this; given negative = v + δ error = v + δ rel_tol direction,
    # we want to pick δ>0 s.t. |v-negative|/rel_tol = δ > max(|v|, |negative|),
    # i.e. δ > |v| and δ² > negative² = (v + δ error)²
    # δ² > v² + rel_tol² δ² + 2δ v·error
    # (1 - rel_tol²) δ² - 2 v·error δ > v²
    #              a δ² - 2 b       δ > c  with :
    a = 1 - rel_tol * rel_tol
    b = v * error
    c = v * v
    δ = (b + sqrt(a * c + b * b)) / a
    note(f"δ: {δ}")

    negative = v + (1 + sqrt(EPSILON)) * max(v.length, δ) * error
    note(
        f"negative example: {negative} = v + {negative - v} = "
        f"v + {(negative - v).length / v.length} * |v| * direction",
    )

    assert not v.isclose(negative, abs_tol=0, rel_tol=rel_tol)


@given(v=vectors())
def test_isclose_negative_tolerances(v: Vector):
    with raises(ValueError):
        v.isclose(v, abs_tol=-1)

    with raises(ValueError):
        v.isclose(v, rel_tol=-1)
