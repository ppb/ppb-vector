import pytest  # type: ignore

from ppb_vector import Vector2


def test_is_iterable():
    test_vector = Vector2(3, 4)
    test_tuple = tuple(test_vector)
    assert test_tuple == (3, 4)



@pytest.mark.parametrize('value', [
    Vector2(1, 2),
    [3, 4],
    (5, 6),
    {'x': 7, 'y': 8},
])
def test_convert(value):
    v = Vector2.convert(value)
    assert isinstance(v, Vector2)
    assert v == value


@pytest.mark.parametrize('value', [
    Vector2(1, 2),
    [3, 4],
    (5, 6),
    {'x': 7, 'y': 8},
])
def test_convert_subclass(value):
    class V(Vector2): pass
    v = V.convert(value)
    assert isinstance(v, V)
    assert v == value
