from typing import Sequence, Union

import hypothesis.strategies as st

from ppb_vector import Vector


def angles():
    return st.floats(min_value=-360, max_value=360)


# The max magnitude of any “sensible” vector
# 10⁷⁵ is a semi-arbitrary choice, but:
# - It is sufficient to describe any game world; even using /picometers/ as the
#   unit of length, the entire observable universe is “only” 9 × 10³⁸ pm across.
# - It is slightly below 10⁷⁷≃2²⁵⁶, so squares are representable without issue
#   in a `float` (or rather an IEEE754 binary64).
MAX_MAGNITUDE = 1e75


def floats(max_magnitude=MAX_MAGNITUDE):
    return st.floats(min_value=-max_magnitude, max_value=max_magnitude)


def lengths(*, min_value=0, max_value=MAX_MAGNITUDE):
    return st.floats(min_value=min_value, max_value=max_value)


def vectors(max_magnitude=MAX_MAGNITUDE):
    return st.builds(
        Vector,
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
    )


def units():
    return st.builds(Vector.x_unit.rotate, angles())


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
BINARY_OPS = (Vector.__add__, Vector.__sub__, Vector.reflect)

# List of (Vector, Vector) -> scalar operations
BINARY_SCALAR_OPS = (Vector.angle, Vector.dot)

# List of (Vector, Vector) -> bool operations
BOOL_OPS = (Vector.__eq__, Vector.isclose)

# List of operations that (Vector, Real) -> Vector
SCALAR_OPS = (Vector.rotate, Vector.scale_by, Vector.scale_to, Vector.truncate)

# List of operations that (Vector) -> Vector
UNARY_OPS = (Vector.__neg__, Vector, Vector.normalize)

# List of (Vector) -> scalar operations
UNARY_SCALAR_OPS = (
    Vector.length.fget,  # type: ignore
    # mypy fails to typecheck properties' attributes:
    #  https://github.com/python/mypy/issues/220
)


# Sequence of vector-likes equivalent to the input vector (def. to the x vector)
def vector_likes(v: Vector = Vector.x_unit):
    return ((v.x, v.y), [v.x, v.y], {"x": v.x, "y": v.y})
