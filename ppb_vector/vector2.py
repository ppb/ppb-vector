import typing
import collections
import functools
from math import acos, atan2, cos, degrees, hypot, isclose, radians, sin, copysign, sqrt
from collections.abc import Sequence, Mapping

__all__ = 'Vector2',


# Vector or subclass
VectorOrSub = typing.TypeVar('VectorOrSub', bound='Vector2')

Realish = typing.Union[float, int]

# Anything convertable to a Vector, including lists, tuples, and dicts
VectorLike = typing.Union[
    'Vector2',  # Or subclasses, unconnected to the VectorOrSub typevar above
    typing.Tuple[typing.SupportsFloat, typing.SupportsFloat],
    typing.Sequence[typing.SupportsFloat],  # TODO: Length 2
    typing.Mapping[str, typing.SupportsFloat],  # TODO: Length 2, keys 'x', 'y'
]


def is_vector_like(value: typing.Any) -> bool:
    return isinstance(value, (Vector2, Sequence, dict))


@functools.lru_cache()
def _find_lowest_type(left: typing.Type, right: typing.Type) -> typing.Type:
    """
    Guess which is the more specific type.
    """
    # Basically, see what classes are unique in each type's MRO and return who
    # has the most.
    lmro = set(left.__mro__)
    rmro = set(right.__mro__)
    lspecial = lmro - rmro
    rspecial = rmro - lmro
    if len(lmro) > len(rmro):
        return left
    elif len(rmro) > len(lmro):
        return right
    else:
        # They're equal, just arbitrarily pick one
        return left


def _find_lowest_vector(left: typing.Type, right: typing.Type) -> typing.Type:
    if left is right:
        return left
    elif not issubclass(left, Vector2):
        return right
    elif not issubclass(right, Vector2):
        return left
    else:
        return _find_lowest_type(left, right)


class Vector2:
    x: float
    y: float

    @typing.overload
    def __init__(self, x: typing.SupportsFloat, y: typing.SupportsFloat): pass

    @typing.overload
    def __init__(self, other: VectorLike): pass

    def __init__(self, *args):
        if len(args) == 1:
            x, y = Vector2.convert(args[0])
        elif len(args) == 2:
            x, y = args
        else:
            raise TypeError(f"Expected 1 vector-like or 2 float-like arguments, got {len(args)}")

        try:
            self.x = x.__float__()
        except AttributeError:
            raise TypeError(f"{type(x).__name__} object not convertable to float")
        try:
            self.y = y.__float__()
        except AttributeError:
            raise TypeError(f"{type(y).__name__} object not convertable to float")

    @classmethod
    def convert(cls: typing.Type[VectorOrSub], value: VectorLike) -> VectorOrSub:
        """
        Constructs a vector from a vector-like. Does not perform a copy.
        """
        # Use Vector2.convert() instead of type(self).convert() so that 
        # _find_lowest_vector() can resolve things well.
        if isinstance(value, cls):
            return value
        elif isinstance(value, Vector2):
            return cls(value.x, value.y)
        elif isinstance(value, Sequence) and len(value) == 2:
            return cls(value[0].__float__(), value[1].__float__())
        elif isinstance(value, Mapping) and 'x' in value and 'y' in value and len(value) == 2:
            return cls(value['x'].__float__(), value['y'].__float__())
        else:
            raise ValueError(f"Cannot use {value} as a vector-like")

    @property
    def length(self) -> float:
        # Surprisingly, caching this value provides no descernable performance
        # benefit, according to microbenchmarks.
        return hypot(self.x, self.y)

    def __len__(self: VectorOrSub) -> int:
        return 2

    def __add__(self: VectorOrSub, other: VectorLike) -> VectorOrSub:
        rtype = _find_lowest_vector(type(other), type(self))
        try:
            other = Vector2.convert(other)
        except ValueError:
            return NotImplemented
        return rtype(self.x + other.x, self.y + other.y)

    def __sub__(self: VectorOrSub, other: VectorLike) -> VectorOrSub:
        rtype = _find_lowest_vector(type(other), type(self))
        try:
            other = Vector2.convert(other)
        except ValueError:
            return NotImplemented
        return rtype(self.x - other.x, self.y - other.y)

    def dot(self: VectorOrSub, other: VectorLike) -> Realish:
        """
        Return the dot product of two vectors.
        """
        other = Vector2.convert(other)
        return self.x * other.x + self.y * other.y

    def scale_by(self: VectorOrSub, other: Realish) -> VectorOrSub:
        """
        Scale by the given amount.
        """
        return type(self)(self.x * other, self.y * other)

    @typing.overload
    def __mul__(self: VectorOrSub, other: VectorLike) -> Realish: pass

    @typing.overload
    def __mul__(self: VectorOrSub, other: Realish) -> VectorOrSub: pass

    def __mul__(self, other):
        """
        Performs a dot product or scale based on other.
        """
        if is_vector_like(other):
            try:
                return self.dot(other)
            except ValueError:
                return NotImplemented
        elif isinstance(other, (float, int)):
            return self.scale_by(other)
        else:
            return NotImplemented

    @typing.overload
    def __rmul__(self: VectorOrSub, other: VectorLike) -> Realish: pass

    @typing.overload
    def __rmul__(self: VectorOrSub, other: Realish) -> VectorOrSub: pass

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self: VectorOrSub, other: Realish) -> VectorOrSub:
        """Perform a division between a vector and a scalar."""
        return type(self)(self.x / other, self.y / other)

    def __getitem__(self: VectorOrSub, item: typing.Union[str, int]) -> Realish:
        if hasattr(item, '__index__'):
            item = item.__index__()  # type: ignore
        if isinstance(item, str):
            if item == 'x':
                return self.x
            elif item == 'y':
                return self.y
            else:
                raise KeyError
        elif isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            else:
                raise IndexError
        else:
            raise TypeError

    def __repr__(self: VectorOrSub) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    def __eq__(self: VectorOrSub, other: typing.Any) -> bool:
        if is_vector_like(other):
            other = Vector2.convert(other)
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self: VectorOrSub, other: typing.Any) -> bool:
        return not (self == other)

    def __iter__(self: VectorOrSub) -> typing.Iterator[Realish]:
        yield self.x
        yield self.y

    def __neg__(self: VectorOrSub) -> VectorOrSub:
        return self.scale_by(-1)

    def angle(self: VectorOrSub, other: VectorLike) -> float:
        other = Vector2.convert(other)

        rv = degrees( atan2(other.x, -other.y) - atan2(self.x, -self.y) )
        # This normalizes the value to (-180, +180], which is the opposite of
        # what Python usually does but is normal for angles
        if rv <= -180:
            rv += 360
        elif rv > 180:
            rv -= 360

        return rv

    def isclose(self: VectorOrSub, other: VectorLike, *,
                abs_tol: Realish=1e-3, rel_tol: Realish=1e-06, rel_to: typing.Sequence[VectorLike]=[]) -> bool:
        """
        Determine whether two vectors are close in value.

           rel_tol
               maximum difference for being considered "close", relative to the
               magnitude of the input values
           rel_to
               additional input values to consider in rel_tol
           abs_tol
               maximum difference for being considered "close", regardless of the
               magnitude of the input values

        Return True if self is close in value to other, and False otherwise.

        For the values to be considered close, the difference between them
        must be smaller than at least one of the tolerances.
        """
        if abs_tol < 0 or rel_tol < 0:
            raise ValueError("Vector2.isclose takes non-negative tolerances")

        other = Vector2.convert(other)

        rel_length = max(
            self.length,
            other.length,
            *map(lambda v: Vector2.convert(v).length, rel_to),
        )

        diff = (self - other).length
        return (
            diff <= rel_tol * rel_length or
            diff <= float(abs_tol)
        )

    @staticmethod
    def _trig(angle: Realish) -> typing.Tuple[float, float]:
        r = radians(angle)
        r_cos, r_sin = cos(r), sin(r)

        if abs(r_cos) > abs(r_sin):
            # From the equation sin(r)² + cos(r)² = 1, we get
            #  sin(r) = ±√(1 - cos(r)²), so we can fix r_sin to that value
            #  preserving its original sign.
            # This way, r_sin² + r_cos² is closer to 1, meaning that the length
            #  of rotated vectors is better preserved
            r_sin = copysign(sqrt(1 - r_cos * r_cos), r_sin)
        else:
            # Same for r_cos
            r_cos = copysign(sqrt(1 - r_sin * r_sin), r_cos)

        return r_cos, r_sin

    def rotate(self: VectorOrSub, angle: Realish) -> VectorOrSub:
        r_cos, r_sin = Vector2._trig(angle)

        x = self.x * r_cos - self.y * r_sin
        y = self.x * r_sin + self.y * r_cos
        return type(self)(x, y)

    def normalize(self: VectorOrSub) -> VectorOrSub:
        return self.scale(1)

    def truncate(self: VectorOrSub, max_length: Realish) -> VectorOrSub:
        if self.length > max_length:
            return self.scale_to(max_length)
        return self

    def scale_to(self: VectorOrSub, length: Realish) -> VectorOrSub:
        """
        Scale the vector to the given length
        """
        if length < 0:
            raise ValueError("Vector2.scale_to takes non-negative lengths.")

        return (length * self) / self.length

    scale = scale_to

    def reflect(self: VectorOrSub, surface_normal: VectorLike) -> VectorOrSub:
        """
        Calculate the reflection of the vector against a given surface normal
        """
        surface_normal = Vector2.convert(surface_normal)
        if not isclose(surface_normal.length, 1):
            raise ValueError("Reflection requires a normalized vector.")

        return self - (2 * (self * surface_normal) * surface_normal)

Sequence.register(Vector2)
