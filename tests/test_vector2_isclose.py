from ppb_vector import Vector2
from pytest import raises # type: ignore
from utils import units, vectors
from hypothesis import assume, given, note, example
from hypothesis.strategies import floats


@given(x=vectors(), abs_tol=floats(min_value=0), rel_tol=floats(min_value=0))
def test_isclose_to_self(x, abs_tol, rel_tol):
    assert x.isclose(x, abs_tol=abs_tol, rel_tol=rel_tol)

@given(x=vectors(max_magnitude=1e75), direction=units(),
       abs_tol=floats(min_value=0, max_value=1e75))
def test_isclose_abs_error(x, direction, abs_tol):
    assert x.isclose(x + (1 - 1e-12) * abs_tol * direction, abs_tol=abs_tol, rel_tol=0)

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
