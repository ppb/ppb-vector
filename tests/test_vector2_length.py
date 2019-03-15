import pytest  # type: ignore

import ppb_vector


@pytest.mark.parametrize(
    "x, y, expected",
    [(6, 8, 10), (8, 6, 10), (0, 0, 0), (-6, -8, 10), (1, 2, 2.23606797749979)],
)
def test_length(x, y, expected):
    vector = ppb_vector.Vector2(x, y)
    assert vector.length == expected
