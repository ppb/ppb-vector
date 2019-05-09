from math import sqrt

from hypothesis import assume, given, note
from hypothesis.strategies import floats
from pytest import raises  # type: ignore

from ppb_vector import Vector
from utils import lengths, units, vectors


@given(x=vectors(), abs_tol=floats(min_value=0), rel_tol=floats(min_value=0))
def test_isclose_to_self(x, abs_tol, rel_tol):
    assert x.isclose(x, abs_tol=abs_tol, rel_tol=rel_tol)


EPSILON = 1e-8


@given(x=vectors(max_magnitude=1e30), direction=units(), abs_tol=lengths(max_value=1e30))
def test_isclose_abs_error(x, direction, abs_tol):
    """Test x.isclose(rel_tol=0) near the boundary between “close” and “not close”

    - x + (1 - ε) * abs_tol * direction should be close
    - x + (1 + ε) * abs_tol * direction shouldn't be close
    """
    assume(abs_tol > EPSILON * x.length)
    note(f"|x|: {x.length}")

    error = abs_tol * direction
    positive = x + (1 - sqrt(EPSILON)) * error
    note(f"positive example: {positive} = x + {positive - x}")
    assert x.isclose(positive, abs_tol=abs_tol, rel_tol=0)

    negative = x + (1 + sqrt(EPSILON)) * abs_tol * direction
    note(f"negative example: {negative} = x + {negative - x}")
    assert not x.isclose(negative, abs_tol=abs_tol, rel_tol=0)


@given(
    x=vectors(max_magnitude=1e30),
    direction=units(),
    rel_tol=floats(min_value=EPSILON, max_value=1 - sqrt(EPSILON)),
)
def test_isclose_rel_error(x, direction, rel_tol):
    """Test x.isclose(abs_tol=0) near the boundary between “close” and “not close”

    - x + (1 - ε) * |x| * rel_tol * direction should always be close
    - We can also generate an example that isn't close,
      though the formula is somewhat complicated.
    """
    assume(x.length > EPSILON)
    note(f"|x| = {x.length}")
    error = rel_tol * direction

    positive = x + (1 - sqrt(EPSILON)) * x.length * error
    note(
        f"positive example: {positive} = x + {positive - x} = "
        f"x + {(positive - x).length / x.length} * |x| * direction",
    )

    assert x.isclose(positive, abs_tol=0, rel_tol=rel_tol)

    # In x.isclose(negative), the allowed relative error is relative to |x|
    # and |negative|, so the acceptable errors grow larger as negative does.
    #
    # We must account for this; given negative = x + δ error = x + δ rel_tol direction,
    # we want to pick δ>0 s.t. |x-negative|/rel_tol = δ > max(|x|, |negative|),
    # i.e. δ > |x| and δ² > negative² = (x + δ error)²
    # δ² > x² + rel_tol² δ² + 2δ x·error
    # (1 - rel_tol²) δ² - 2 x·error δ > x²
    #              a δ² - 2 b       δ > c  with :
    a = 1 - rel_tol * rel_tol
    b = x * error
    c = x * x
    δ = (b + sqrt(a * c + b * b)) / a
    note(f"δ: {δ}")

    negative = x + (1 + sqrt(EPSILON)) * max(x.length, δ) * error
    note(
        f"negative example: {negative} = x + {negative - x} = "
        f"x + {(negative - x).length / x.length} * |x| * direction",
    )

    assert not x.isclose(negative, abs_tol=0, rel_tol=rel_tol)


def test_isclose_negative_tolerances():
    zero = Vector(0, 0)

    with raises(ValueError):
        zero.isclose(zero, abs_tol=-1)

    with raises(ValueError):
        zero.isclose(zero, rel_tol=-1)
