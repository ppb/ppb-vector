import ppb_vector


def test_is_iterable():
    test_vector = ppb_vector.Vector2(3, 4)
    test_tuple = tuple(test_vector)
    print(test_tuple)
    assert test_tuple[0] == 3
    assert test_tuple[1] == 4
