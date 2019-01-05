import pytest

from ppb_vector import Vector2


negation_data = (
    (Vector2(1, 1), Vector2(-1, -1)),
    (Vector2(2, -3), Vector2(-2, 3)),
    (Vector2(-4, 18), Vector2(4, -18))
)


@pytest.mark.parametrize('test_vector, expected_result', negation_data)
def test_negation(test_vector, expected_result):
    assert -test_vector == expected_result
