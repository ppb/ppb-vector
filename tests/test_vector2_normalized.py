import ppb_vector


def test_normalized():
    test_vector = ppb_vector.Vector2(5, 5)
    test_vector_normalized = test_vector.normalize()
    assert test_vector_normalized == ppb_vector.Vector2(0.7071067811865475, 0.7071067811865475)
