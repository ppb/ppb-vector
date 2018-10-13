from ppb_vector import Vector2
import pytest

@pytest.mark.parametrize("left, right, expected", [
    (Vector2(1, 1), Vector2(0, -1), -1),
    (Vector2(1, 1), Vector2(-1, 0), 1),
    (Vector2(0, 1), Vector2(0, -1), 0),
    (Vector2(-1, -1), Vector2(1, 0), 1),
    (Vector2(-1, -1), Vector2(-1, 0), -1)
])
def test_cross(left, right, expected):
    assert left ^ right == expected
    assert right ^ left == -expected
