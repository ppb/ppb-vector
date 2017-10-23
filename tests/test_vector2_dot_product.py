import ppb_vector


def test_dot_product():
    vector_one = ppb_vector.Vector2(-1,2)
    vector_two = ppb_vector.Vector2(3,4)
    vector_result = vector_one * vector_two
    print(vector_result)

    assert vector_result == 5
 
 
