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
        event("Negative example generated (abs_tol > EPSILON * x.length)")
        note(f"negative example: {negative} = x + {negative - x}")
        assert not x.isclose(negative, abs_tol=abs_tol, rel_tol=0)


@given(x=vectors(), direction=units(),
       rel_tol=floats(min_value=0, max_value=1e75))
def test_isclose_rel_error(x, direction, rel_tol):
    assert x.isclose(x + rel_tol * x.length * direction, abs_tol=0, rel_tol=rel_tol)


def test_isclose_negative_tolerances():
    zero = Vector2(0, 0)

    with raises(ValueError):
        zero.isclose(zero, abs_tol=-1)

    with raises(ValueError):
        zero.isclose(zero, rel_tol=-1)
