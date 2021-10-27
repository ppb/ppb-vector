from ppb_vector import Vector


def test_u():
    assert Vector.u == (1, 0)


def test_v():
    assert Vector.v == (0, 1)


def test_uv_angle():
    assert Vector.u.angle(Vector.v) == 90


def test_zero():
    assert not Vector.zero
