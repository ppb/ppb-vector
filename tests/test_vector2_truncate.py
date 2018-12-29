import pytest  # type: ignore
from hypothesis import assume, example, given, note
from hypothesis.strategies import floats
from typing import Type, Union
from utils import vectors

from ppb_vector import Vector2


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
def test_truncate_length(x: Vector2, max_length: float):
    assert x.truncate(max_length).length <= (1 + 1e-14) * max_length


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
def test_truncate_invariant(x: Vector2, max_length: float):
    assume(x.length <= max_length)
    assert x.truncate(max_length) == x


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
@example( # Large example where x.length == max_length but 1 * x != x
    x=Vector2(0.0, 7.387424005855793e+62), max_length=7.387424005855793e+62
)
def test_truncate_equivalent_to_scale(x: Vector2, max_length: float):
    """Vector2.scale_to and truncate are equivalent when max_length <= x.length"""
    assume(max_length <= x.length)
    note(f"x.length = {x.length}")
    if max_length > 0:
        note(f"x.length = {x.length / max_length} * max_length")

    scale    : Union[Vector2, Type[Exception]]
    truncate : Union[Vector2, Type[Exception]]

    try:
        truncate = x.truncate(max_length)
    except Exception as e:
        truncate = type(e)

    try:
        scale = x.scale_to(max_length)
    except Exception as e:
        scale = type(e)

    assert scale == truncate
