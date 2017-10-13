import ppb_vector


def test_truncate():
    test_vector = ppb_vector.Vector2(700, 500)
    test_vector_truncated = test_vector.truncate(5)
    print(test_vector_truncated)
    assert test_vector_truncated == ppb_vector.Vector2(4.068667356033675, 2.906190968595482)
