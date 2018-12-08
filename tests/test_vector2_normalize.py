import pytest  # type: ignore

import ppb_vector


@pytest.mark.parametrize("x, y", [
    (3, 4),
    (6, 8),
    (0, 1),
    (1, 0),
])
def test_normalize(x, y):
    vector = ppb_vector.Vector2(x, y).normalize()
    assert vector.length == 1
