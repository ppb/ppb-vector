from ppb_vector import Vector


def test_u():
    assert Vector.x_unit == (1, 0)


def test_v():
    assert Vector.y_unit == (0, 1)


def test_uv_angle():
    assert Vector.x_unit.angle(Vector.y_unit) == 90


def test_zero():
    assert not Vector.zero
