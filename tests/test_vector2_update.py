from hypothesis import given

from ppb_vector import Vector
from utils import floats, vectors


@given(v=vectors(), x=floats())
def test_update_x(v: Vector, x: float):
    assert v.update(x=x) == (x, v.y)


@given(v=vectors(), y=floats())
def test_update_y(v: Vector, y: float):
    assert v.update(y=y) == (v.x, y)


@given(v=vectors(), x=floats(), y=floats())
def test_update_xy(v: Vector, x: float, y: float):
    assert v.update(x=x, y=y) == (x, y)
