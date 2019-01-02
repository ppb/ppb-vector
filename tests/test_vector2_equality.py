import ppb_vector

def test_equal():
  test_vector_1 = ppb_vector.Vector2(50, 800)
  test_vector_2 = ppb_vector.Vector2(50, 800)

  assert test_vector_1 == test_vector_2

def test_not_equal():
  test_vector_1 = ppb_vector.Vector2(800, 800)
  test_vector_2 = ppb_vector.Vector2(50, 800)

  assert test_vector_1 != test_vector_2
