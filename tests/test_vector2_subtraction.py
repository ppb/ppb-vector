import ppb_vector


def test_subtraction():
    vector_one = ppb_vector.Vector2(3, 3)
    vector_two = ppb_vector.Vector2(2, 1)
    vector_result = vector_one - vector_two
    print(vector_result)

    assert vector_result == ppb_vector.Vector2(1, 2)
