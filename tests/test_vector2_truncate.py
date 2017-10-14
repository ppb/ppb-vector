import pytest
from ppb_vector import Vector2

def test_truncate_larger_max_length():
    vector = Vector2(3, 5)
    truncated = vector.truncate(10)
    assert vector == truncated

def test_truncate_equal_max_length():
    vector = Vector2(3, 4)
    truncated = vector.truncate(5)
    assert vector == truncated
    
def test_truncate_lesser_max_length():
    vector = Vector2(20, 30)
    truncated = vector.truncate(10)
    assert truncated == vector.scale(10)
