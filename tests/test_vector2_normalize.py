from math import hypot
from ppb_vector import Vector2
import pytest

test_data = [
    (Vector2(1, 0), Vector2(1, 0)),
    (Vector2(2, 2), Vector2(2, 2) * (1 / hypot(2, 2))),
    (Vector2(31, -15), Vector2(31, -15) * (1 / hypot(31, -15))),
    (Vector2(0, 0), Vector2(0, 0)),
]


@pytest.mark.parametrize("vector, expected", test_data)
def test_length(vector, expected):
    normalized = vector.normalize()
    assert normalized == expected
