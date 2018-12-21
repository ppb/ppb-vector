import pytest  # type: ignore
from hypothesis import assume, given
from hypothesis.strategies import floats
from typing import Type, Union
from utils import vectors

from ppb_vector import Vector2


def test_truncate():
    test_vector = Vector2(700, 500)
    test_vector_truncated = test_vector.truncate(5)
    print(test_vector_truncated)
    assert test_vector_truncated == Vector2(4.068667356033675, 2.906190968595482)


def test_truncate_lesser_max_length():
    vector = Vector2(20, 30)
    truncated = vector.truncate(10)
    assert truncated == vector.scale(10)


data = [
    ([Vector2(5, 12), 6], Vector2(5, 12).scale(6)),
    ([Vector2(92, 19), 61], Vector2(92, 19).scale(61)),
    ([Vector2(2212481, 189898), 129039], Vector2(2212481, 189898).scale(129039)),
    ([Vector2(155, 155), 155], Vector2(155, 155).scale(155))
]


@pytest.mark.parametrize('test_input, expected', data)
def test_multiples_values(test_input, expected):
    assert test_input[0].truncate(test_input[1]) == expected


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
def test_truncate_length(x: Vector2, max_length: float):
    assert x.truncate(max_length).length <= max_length


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
def test_truncate_invariant(x: Vector2, max_length: float):
    assume(x.length <= max_length)
    assert x.truncate(max_length) == x


@given(x=vectors(max_magnitude=1e75), max_length=floats(min_value=0, max_value=1e75))
def test_truncate_equivalent_to_scale(x: Vector2, max_length: float):
    """Vector2.scale_to and truncate are equivalent when max_length <= x.length"""
    assume(max_length <= x.length)

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
