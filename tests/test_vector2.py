import pytest  # type: ignore

from ppb_vector import Vector2


def test_is_iterable():
    test_vector = Vector2(3, 4)
    test_tuple = tuple(test_vector)
    assert test_tuple == (3, 4)

negation_data = (
    (Vector2(1, 1), Vector2(-1, -1)),
    (Vector2(2, -3), Vector2(-2, 3)),
    (Vector2(-4, 18), Vector2(4, -18))
)


@pytest.mark.parametrize('test_vector, expected_result', negation_data)
def test_negation(test_vector, expected_result):
    assert -test_vector == expected_result
