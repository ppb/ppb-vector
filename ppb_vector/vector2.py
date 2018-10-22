import typing
import collections
import functools
from math import acos, atan2, cos, degrees, hypot, isclose, radians, sin
from numbers import Real
from collections.abc import Sequence

__all__ = 'Vector2',


# Vector or subclass
VectorOrSub = typing.TypeVar('VectorOrSub', bound='Vector2')

# Anything convertable to a Vector, including lists, tuples, and dicts
VectorLike = typing.Union[
    VectorOrSub,
    typing.List[Real],  # TODO: Length 2
    typing.Tuple[Real, Real],
    typing.Dict[str, Real],  # TODO: Length 2, keys 'x', 'y'
]

Realish = typing.Union[Real, float, int]


def is_vector_like(value: typing.Any) -> bool:
    return isinstance(value, (Vector2, list, tuple, dict))


_fakevector = collections.namedtuple('_fakevector', ['x', 'y'])

def _mkvector(value, *, castto=_fakevector):
    if isinstance(value, Vector2):
        return value
    # FIXME: Allow all types of sequences
    elif isinstance(value, (list, tuple)) and len(value) == 2:
        return castto(value[0], value[1])
    # FIXME: Allow all types of mappings
    elif isinstance(value, dict) and 'x' in value and 'y' in value and len(value) == 2:
        return castto(value['x'], value['y'])
    else:
        raise ValueError(f"Cannot use {value} as a vector-like")


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
    x: Realish
    y: Realish
    length: Realish

    def __init__(self: VectorOrSub, x: Realish, y: Realish):
        try:
            self.x = x.__float__()
        except AttributeError:
            raise TypeError(f"{type(x).__name__} object not convertable to float")
        try:
            self.y = y.__float__()
        except AttributeError:
            raise TypeError(f"{type(y).__name__} object not convertable to float")
        self.length = hypot(self.x, self.y)

    @classmethod
    def convert(cls: typing.Type[VectorOrSub], value: VectorLike) -> VectorOrSub:
        """
        Constructs a vector from a vector-like.
        """
        fake = _mkvector(value)
        return cls(fake.x, fake.y)

    def __len__(self: VectorOrSub) -> int:
        return 2

    def __add__(self: VectorOrSub, other: VectorLike) -> VectorOrSub:
        try:
            other = _mkvector(other)
        except ValueError:
            return NotImplemented
        rtype = _find_lowest_vector(type(other), type(self))
        return rtype(self.x + other.x, self.y + other.y)

    def __sub__(self: VectorOrSub, other: VectorLike) -> VectorOrSub:
        try:
            other = _mkvector(other)
        except ValueError:
            return NotImplemented
        rtype = _find_lowest_vector(type(other), type(self))
        return rtype(self.x - other.x, self.y - other.y)

    def dot(self: VectorOrSub, other: VectorLike) -> Real:
        """
        Return the dot product of two vectors.
        """
        other = _mkvector(other)
        return self.x * other.x + self.y * other.y

    def scale_by(self: VectorOrSub, other: Realish) -> VectorOrSub:
        """
        Scale by the given amount.
        """
        return type(self)(self.x * other, self.y * other)

    def __mul__(self: VectorOrSub, other: typing.Union[VectorLike, Realish]) -> typing.Union[VectorOrSub, Realish]:
        """
        Performs a dot product or scale based on other.
        """
        if is_vector_like(other):
            try:
                return self.dot(other)
            except ValueError:
                return NotImplemented
        elif isinstance(other, Real):
            return self.scale_by(other)
        else:
            return NotImplemented

    def __rmul__(self: VectorOrSub, other: typing.Union[VectorLike, Realish]) -> typing.Union[VectorOrSub, Realish]:
        return self.__mul__(other)

    def __xor__(self: VectorOrSub, other: VectorLike) -> Real:
        """
        Computes the magnitude of the cross product
        """
        other = _mkvector(other)
        return self.x * other.y - self.y * other.x

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

    def __eq__(self: VectorOrSub, other: VectorLike) -> bool:
        if is_vector_like(other):
            other = _mkvector(other)
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self: VectorOrSub, other: VectorLike) -> bool:
        if is_vector_like(other):
            other = _mkvector(other)
            return self.x != other.x or self.y != other.y
        else:
            return True

    def __iter__(self: VectorOrSub) -> typing.Iterator[Realish]:
        yield self.x
        yield self.y

    def __neg__(self: VectorOrSub) -> VectorOrSub:
        return self.scale_by(-1)

    def angle(self: VectorOrSub, other: VectorLike) -> float:
        other = _mkvector(other, castto=Vector2)

        rv = degrees( atan2(other.x, -other.y) - atan2(self.x, -self.y) )
        # This normalizes the value to (-180, +180], which is the opposite of
        # what Python usually does but is normal for angles
        if rv <= -180:
            rv += 360
        elif rv > 180:
            rv -= 360

        return rv

    def isclose(self: VectorOrSub, other: VectorLike, *, rel_tol: Realish=1e-06, abs_tol: Realish=1e-3) -> bool:
        """
        Determine whether two vectors are close in value.

           rel_tol
               maximum difference for being considered "close", relative to the
               magnitude of the input values
            abs_tol
               maximum difference for being considered "close", regardless of the
               magnitude of the input values
        
        Return True if self is close in value to other, and False otherwise.
        
        For the values to be considered close, the difference between them
        must be smaller than at least one of the tolerances.
        """
        other = _mkvector(other, castto=Vector2)
        diff = (self - other).length
        return (
            diff < rel_tol * self.length or
            diff < rel_tol * other.length or 
            diff < abs_tol
        )

    def rotate(self: VectorOrSub, degrees: Realish) -> VectorOrSub:
        r = radians(degrees)
        r_cos = cos(r)
        r_sin = sin(r)

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
        try:
            scale = length / self.length
        except ZeroDivisionError:
            scale = 1
        return self.scale_by(scale)

    scale = scale_to

    def reflect(self: VectorOrSub, surface_normal: VectorLike) -> VectorOrSub:
        """
        Calculate the reflection of the vector against a given surface normal
        """
        surface_normal = _mkvector(surface_normal, castto=Vector2)
        if not isclose(surface_normal.length, 1):
            raise ValueError("Reflection requires a normalized vector.")

        return self - (2 * (self * surface_normal) * surface_normal)

Sequence.register(Vector2)
