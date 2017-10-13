import ppb_vector


def test_addition():
    vector_one = ppb_vector.Vector2(1, 0)
    vector_two = ppb_vector.Vector2(0, 1)
    vector_result = vector_one + vector_two
    print(vector_result)

    assert vector_result == ppb_vector.Vector2(1, 1)
