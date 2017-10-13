import ppb_vector

def test_length():
    #Vector length is the sqrt(x*x+y*y)
    #For Vector(3,4) the correct length is 5.0

    vector = ppb_vector.Vector2(3, 4)
    assert vector.length == 5.0
