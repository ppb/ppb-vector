from ppb_vector import Vector2
from hypothesis import note
from typing import Sequence, Union
import hypothesis.strategies as st


def angles():
    return st.floats(min_value=-360, max_value=360)

def floats(max_magnitude=1e75):
    return st.floats(min_value=-max_magnitude, max_value=max_magnitude)

def lengths(min_value=0, max_value=1e75):
    return st.floats(min_value=min_value, max_value=max_value)

def vectors(max_magnitude=1e75):
    return st.builds(Vector2,
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude),
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude)
    )

def units():
    return st.builds(Vector2(1, 0).rotate, angles())


def angle_isclose(x, y, epsilon = 6.5e-5):
    d = (x - y) % 360
    return (d < epsilon) or (d > 360 - epsilon)

def isclose(x, y, abs_tol: float=1e-9, rel_tol: float=1e-9, rel_exp: float=1,
            rel_to: Sequence[Union[float, Vector2]]=[]):
    if rel_exp < 1:
        raise ValueError(f"Expected rel_exp >= 1, got {rel_exp}")

    diff = abs(x - y)
    rel_max = max(abs(x), abs(y),
                  *(abs(z) ** rel_exp for z in rel_to if isinstance(z, float)),
                  *(z.length ** rel_exp for z in rel_to if isinstance(z, Vector2))
    )
    note(f"rel_max = {rel_max}")
    if rel_max > 0:
        note(f"diff = {diff} = {diff/rel_max} * rel_max")
    else:
        note(f"diff = {diff}")

    return diff <= rel_max * rel_tol or diff <= abs_tol


# List of operations that (Vector2, Vector2) -> Vector2
BINARY_OPS = [
    Vector2.__add__,
    Vector2.__sub__,
    Vector2.reflect,
]

# List of (Vector2, Vector2) -> scalar operations
BINARY_SCALAR_OPS = [
    Vector2.angle,
    Vector2.dot,
]

# List of (Vector2, Vector2) -> bool operations
BOOL_OPS = [
    Vector2.__eq__,
    Vector2.isclose,
]

# List of operations that (Vector2, Real) -> Vector2
SCALAR_OPS = [
    Vector2.rotate,
    Vector2.scale_by,
    Vector2.scale_to,
    Vector2.truncate,
]

# List of operations that (Vector2) -> Vector2
UNARY_OPS = [
    Vector2.__neg__,
    Vector2.convert,
    Vector2.normalize,
]

# List of (Vector2) -> scalar operations
UNARY_SCALAR_OPS = [
    Vector2.length.fget, # type: ignore
                         # mypy fails to typecheck properties' attributes:
                         #  https://github.com/python/mypy/issues/220
]


# Sequence of vector-likes equivalent to the x unit vector
UNIT_VECTOR_LIKES = (
    (0, 1), [0, 1], {"x": 0, "y": 1}
)
