import pytest  # type: ignore

from ppb_vector import Vector


data = [
    ((0, 1),   (0, 1),    (0, 0)),
    ((4, 6),   (1, 1),    (3, 5)),
    ((3, 7),   (1, 3),    (2, 4)),
    ((7, 11),  (3, 5),    (4, 6)),
    ((10, 16), (2, 2),    (8, 14)),
    ((25, 22), (22, 61),  (3, -39)),
    ((39, 43), (92, -12), (-53, 55)),
    ((1, 1),   (2, 2),    (-1, -1)),
    ((25, 22), (12, 92),  (13, -70)),
    ((42, 12), (-5, 23),  (47, -11)),
    ((51, 28), (72, 31),  (-21, -3)),
    ((1, 2),   (2, 2),    (-1, 0)),
]


@pytest.mark.parametrize("x, y, expected", data)
def test_multiples_values(x, y, expected):
    assert (Vector(x) - y) == expected
