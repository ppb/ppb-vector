from ppb_vector import Vector2
from pytest import raises # type: ignore
from utils import units, lengths, vectors
from hypothesis import assume, event, given, note, example
from hypothesis.strategies import floats


@given(x=vectors(), abs_tol=floats(min_value=0), rel_tol=floats(min_value=0))
def test_isclose_to_self(x, abs_tol, rel_tol):
    assert x.isclose(x, abs_tol=abs_tol, rel_tol=rel_tol)


@given(x=vectors(), direction=units(), abs_tol=lengths())
def test_isclose_abs_error(x, direction, abs_tol):
    """Test x.isclose(rel_tol=0) near the boundary between “close” and “not close”

    - x + (1 - EPSILON) * abs_tol * direction should always be close
    - x + (1 + EPSILON) * abs_tol * direction should not be close
      assuming it isn't equal to x (because of rounding, or because x is null)
    """
    error = abs_tol * direction
    note(f"error = {error}")

    EPSILON = 1e-12
    positive = x + (1 - EPSILON) * error
    note(f"positive example: {positive} = x + {positive - x}")
    assert x.isclose(positive, abs_tol=abs_tol, rel_tol=0)

    if abs_tol > EPSILON * x.length:
        negative = x + (1 + EPSILON) * error
        event("Negative example generated (abs_tol > ε * |x|)")
        note(f"negative example: {negative} = x + {negative - x}")
        assert not x.isclose(negative, abs_tol=abs_tol, rel_tol=0)


EPSILON = 1e-8
@given(x=vectors(), direction=units(),
       rel_tol=floats(min_value=EPSILON, max_value=1-EPSILON))
def test_isclose_rel_error(x, direction, rel_tol):
    """Test x.isclose(abs_tol=0) near the boundary between “close” and “not close”

    - x + rel_tol * |x| * direction should always be close
    - x + (1 + EPSILON) * rel_tol * |x| * direction should not be close
      assuming it isn't equal to x (because of rounding, or because x is null)
    """
    error = rel_tol * x.length * direction
    note(f"error = {error}")

    positive = x + (1 - EPSILON) * error
    note(f"positive example: {positive} = x + {positive - x}")
    if x.length > EPSILON:
        note(f"x + |x| * {(positive - x) / x.length}")

    assert x.isclose(positive, abs_tol=0, rel_tol=rel_tol)

    if x.length > EPSILON:
        # In x.isclose(negative), the allowed relative error is relative to |x|
        # and |negative|, so the acceptable errors grow larger as negative does.
        #
        # The choice of negative accounts for this, with the (1 - rel_tol) term:
        # we have negative = x + Δ, and we want to pick Δ such that
        # δ = |x - negative| > rel_tol * max(|x|, |negative|)
        #
        # Since r * (|x| + δ) > rel_tol * max(|x|, |negative|), any choice where
        # δ > rel_tol * (|x| + δ) is suitable. The smallest is
        # rel_tol |x| / (1 - rel_tol), as such, we take
        # Δ = r * |x| * direction / (1 - rel_tol), and an ε safety margin.
        negative = x + (1 + EPSILON) / (1 - rel_tol) * error
        note(f"negative example: {negative} = x + {negative - x} = "
             f"x + {(negative - x).length / x.length} * |x| * {(negative - x).normalize()}")

        assert not x.isclose(negative, abs_tol=0, rel_tol=rel_tol)


def test_isclose_negative_tolerances():
    zero = Vector2(0, 0)

    with raises(ValueError):
        zero.isclose(zero, abs_tol=-1)

    with raises(ValueError):
        zero.isclose(zero, rel_tol=-1)
