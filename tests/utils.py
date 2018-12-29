from ppb_vector import Vector2
import hypothesis.strategies as st


def vectors(max_magnitude=1e75):
    return st.builds(Vector2,
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude),
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude)
    )

@st.composite
def units(draw, elements=st.floats(min_value=0, max_value=360)):
    angle = draw(elements)
    return Vector2(1, 0).rotate(angle)


def angle_isclose(x, y, epsilon = 6.5e-5):
    d = (x - y) % 360
    return (d < epsilon) or (d > 360 - epsilon)


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
