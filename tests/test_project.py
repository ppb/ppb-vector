from math import sqrt

from hypothesis import given, reject

from ppb_vector import Vector
from utils import angle_isclose, floats, MAX_MAGNITUDE, units, vectors


# TODO(nicoo): Replace with Vector.zero once #168 is merged.
ZERO = Vector(0, 0)
EPSILON = 1e-8


@given(v=vectors())
def test_project_canonical(v: Vector):
    """Decomposition against the canonical (x, y) basis is trivial."""
    assert v.project((1, 0)) == (v.x, 0)
    assert v.project((0, 1)) == (0, v.y)


@given(v=vectors(), direct=units())
def test_project_recombine(v: Vector, direct: Vector):
    """A vector is the sum of its orthogonal projections."""
    assert v.isclose(v.project(direct) + v.project(direct.rotate(90)))


@given(v=vectors(), direct=units())
def test_project_angles(v: Vector, direct: Vector):
    """Projections are colinear to the direction."""
    assert angle_isclose(v.project(direct).angle(direct), 0, modulus=180) or v.isclose(ZERO)


@given(
    # We need |λv| ⩽ MAX_MAGNITUDE; picking |λ| and |v| below √MAX_MAGNITUDE
    #  achieves that, though rejects some otherwise-valid combinations.
    v=vectors(), w=vectors(max_magnitude=sqrt(MAX_MAGNITUDE)),
    direct=units(), λ=floats(max_magnitude=sqrt(MAX_MAGNITUDE)),
)
def test_project_linear(v: Vector, w: Vector, λ: float, direct: Vector):
    """Projections are linear maps."""
    inner = (v + λ * w).project(direct)
    outer = v.project(direct) + λ * w.project(direct)

    assert inner.isclose(outer)


@given(v=vectors(), λ=floats(), direct=units())
def test_project_invariant(v: Vector, λ: float, direct: Vector):
    """Projection isn't changed by scaling the direction."""
    if (λ * direct).isclose(ZERO):
        reject()
    assert v.project(direct).isclose(v.project(λ * direct))
