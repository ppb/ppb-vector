from hypothesis import given

from ppb_vector import Vector2
from utils import floats, vectors


@given(v=vectors(), x=floats())
def test_update_x(v: Vector2, x: float):
    assert v.update(x=x) == (x, v.y)


@given(v=vectors(), y=floats())
def test_update_y(v: Vector2, y: float):
    assert v.update(y=y) == (v.x, y)


@given(v=vectors(), x=floats(), y=floats())
def test_update_xy(v: Vector2, x: float, y: float):
    assert v.update(x=x, y=y) == (x, y)
