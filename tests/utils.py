def angle_isclose(x, y, epsilon = 6.5e-5):
    d = (x - y) % 360
    return (d < epsilon) or (d > 360 - epsilon)
