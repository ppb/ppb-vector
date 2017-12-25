from ppb_vector import Vector2
import pytest

reflect_data = (
    (Vector2(1, 1), Vector2(0, -1), Vector2(1, -1)),
    (Vector2(1, 1), Vector2(-1, 0), Vector2(-1, 1)),
    (Vector2(0, 1), Vector2(0, -1), Vector2(0, -1)),
    (Vector2(-1, -1), Vector2(1, 0), Vector2(1, -1)),
    (Vector2(-1, -1), Vector2(-1, 0), Vector2(-1,1))
)


@pytest.mark.parametrize("initial_vector, surface_normal, expected_vector", reflect_data)
def test_reflect(initial_vector, surface_normal, expected_vector):
    assert initial_vector.reflect(surface_normal) == expected_vector
