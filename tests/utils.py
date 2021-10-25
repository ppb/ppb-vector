from typing import Sequence, Union

import hypothesis.strategies as st

from ppb_vector import Vector


UNIT_X, UNIT_Y = Vector(1, 0), Vector(0, 1)


def angles():
    return st.floats(min_value=-360, max_value=360)


def floats(max_magnitude=1e75):
    return st.floats(min_value=-max_magnitude, max_value=max_magnitude)


def lengths(*, min_value=0, max_value=1e75):
    return st.floats(min_value=min_value, max_value=max_value)


def vectors(max_magnitude=1e75):
    return st.builds(
        Vector,
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
    )


def units():
    return st.builds(UNIT_X.rotate, angles())


def angle_isclose(x, y, *, epsilon=6.5e-5, modulus=360):
    d = (x - y) % modulus
    return (d < epsilon) or (d > modulus - epsilon)


def isclose(
    x,
    y,
    *,
    abs_tol: float = 1e-9,
    rel_tol: float = 1e-9,
    rel_exp: float = 1,
    rel_to: Sequence[Union[float, Vector]] = (),
):
    if rel_exp < 1:
        raise ValueError(f"Expected rel_exp >= 1, got {rel_exp}")

    diff = abs(x - y)
    rel_max = max(
        abs(x),
        abs(y),
        *(abs(z) ** rel_exp for z in rel_to if isinstance(z, float)),
        *(z.length ** rel_exp for z in rel_to if isinstance(z, Vector)),
    )

    return diff <= rel_max * rel_tol or diff <= abs_tol


# List of operations that (Vector, Vector) -> Vector
BINARY_OPS = frozenset({Vector.__add__, Vector.__sub__, Vector.reflect})

# List of (Vector, Vector) -> scalar operations
BINARY_SCALAR_OPS = frozenset({Vector.angle, Vector.dot})

# List of (Vector, Vector) -> bool operations
BOOL_OPS = frozenset({Vector.__eq__, Vector.isclose})

# List of operations that (Vector, Real) -> Vector
SCALAR_OPS = frozenset({
    Vector.rotate, Vector.scale_by, Vector.scale_to, Vector.truncate,
})

# List of operations that (Vector) -> Vector
UNARY_OPS = frozenset({Vector.__neg__, Vector, Vector.normalize})

# List of (Vector) -> scalar operations
UNARY_SCALAR_OPS = frozenset({
    Vector.length.fget,  # type: ignore
    # mypy fails to typecheck properties' attributes:
    #  https://github.com/python/mypy/issues/220
})


# Sequence of vector-likes equivalent to the input vector (def. to the x vector)
def vector_likes(v: Vector = UNIT_X):
    return ((v.x, v.y), [v.x, v.y], {"x": v.x, "y": v.y})
