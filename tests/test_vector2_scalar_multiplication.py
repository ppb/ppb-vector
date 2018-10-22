import pytest  # type: ignore
from ppb_vector import Vector2


@pytest.mark.parametrize("x, y, expected", [
    (Vector2(6, 1), 0, Vector2(0, 0)),
    (Vector2(6, 1), 2, Vector2(12, 2)),
    (Vector2(0, 0), 3, Vector2(0, 0)),
    (Vector2(-1.5, 2.4), -2, Vector2(3.0, -4.8)),
    (Vector2(1, 2), 0.1, Vector2(0.1, 0.2))
])
def test_scalar_multiplication(x, y, expected):
    assert x * y == expected
