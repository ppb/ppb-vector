import pytest
from ppb_vector import Vector2


def test_truncate_larger_max_length():
    vector = Vector2(3, 5)
    truncated = vector.truncate(10)
    assert vector == truncated


def test_truncate_equal_max_length():
    vector = Vector2(3, 4)
    truncated = vector.truncate(5)
    assert vector == truncated


def test_truncate_lesser_max_length():
    vector = Vector2(20, 30)
    truncated = vector.truncate(10)
    assert truncated == vector.scale(10)


data = [
	([Vector2(1, 2), 3], Vector2(1, 2)),
	([Vector2(5, 12), 6], Vector2(5, 12).scale(6)),
	([Vector2(92, 19), 61], Vector2(92, 19).scale(61)),
	([Vector2(22, 5), 41], Vector2(22, 5)),
	([Vector2(2212481, 189898), 129039], Vector2(2212481, 189898).scale(129039)),
	([Vector2(5, 12), 13], Vector2(5, 12)),
	([Vector2(438, 153), 464], Vector2(438, 153)),
	([Vector2(155, 155), 155], Vector2(155, 155).scale(155))
]


@pytest.mark.parametrize('test_input, expected', data)
def test_multiples_values(test_input, expected):
    assert test_input[0].truncate(test_input[1]) == expected