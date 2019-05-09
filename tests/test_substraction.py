import pytest  # type: ignore

from ppb_vector import Vector


data = [
    ([Vector(0, 1), Vector(0, 1)], Vector(0, 0)),
    ([Vector(4, 6), Vector(1, 1)], Vector(3, 5)),
    ([Vector(3, 7), Vector(1, 3)], Vector(2, 4)),
    ([Vector(7, 11), Vector(3, 5)], Vector(4, 6)),
    ([Vector(10, 16), Vector(2, 2)], Vector(8, 14)),
    ([Vector(25, 22), Vector(22, 61)], Vector(3, -39)),
    ([Vector(39, 43), Vector(92, -12)], Vector(-53, 55)),
    ([Vector(1, 1), (2, 2)], Vector(-1, -1)),
    ([Vector(25, 22), (12, 92)], Vector(13, -70)),
    ([Vector(42, 12), (-5, 23)], Vector(47, -11)),
    ([Vector(51, 28), [72, 31]], Vector(-21, -3)),
    ([Vector(1, 2), [2, 2]], Vector(-1, 0)),
]


@pytest.mark.parametrize("test_input, expected", data)
def test_multiples_values(test_input, expected):
    assert (test_input[0] - test_input[1]) == expected
