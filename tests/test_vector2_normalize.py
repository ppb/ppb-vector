import pytest  # type: ignore

import ppb_vector


@pytest.mark.parametrize("x, y, expected", [
    (3, 4, 1),
    (6, 8, 1),
    (0, 1, 1),
    (1, 0, 1),
    (0, 0, 0)
])
def test_normalize(x, y, expected):
    vector = ppb_vector.Vector2(x, y).normalize()
    assert vector.length == expected
