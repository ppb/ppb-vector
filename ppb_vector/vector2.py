import typing
import collections
from math import acos, cos, degrees, hypot, radians, sin
from numbers import Real
from collections.abc import Sequence

__all__ = 'Vector2',


VectorLike = typing.Union[
    'Vector2',
    typing.List[Real],  # TODO: Length 2
    typing.Tuple[Real, Real],
    typing.Dict[str, Real],  # TODO: Length 2, keys 'x', 'y'
]


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


class Vector2(Sequence):

    def __init__(self, x: Real, y: Real):
        self.x = x
        self.y = y
        self.length = hypot(x, y)

    @classmethod
    def convert(cls, value: VectorLike) -> 'Vector2':
        """
        Constructs a vector from a vector-like.
        """
        return _mkvector(value, castto=type(cls))

    def __len__(self) -> int:
        return 2

    def __add__(self, other: VectorLike) -> 'Vector2':
        try:
            other = _mkvector(other)
        except ValueError:
            return NotImplemented
        rtype = type(other) if isinstance(other, Vector2) else type(self)
        return rtype(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorLike) -> 'Vector2':
        try:
            other = _mkvector(other)
        except ValueError:
            return NotImplemented
        rtype = type(other) if isinstance(other, Vector2) else type(self)
        return rtype(self.x - other.x, self.y - other.y)

    def __mul__(self, other: VectorLike) -> 'Vector2':
        if is_vector_like(other):
            try:
                other = _mkvector(other)
            except ValueError:
                return NotImplemented
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Real):
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other: VectorLike) -> 'Vector2':
        return self.__mul__(other)

    def __xor__(self, other: VectorLike) -> Real:
        """
        Computes the magnitude of the cross product
        """
        other = _mkvector(other)
        return self.x * other.y - self.y * other.x

    def __getitem__(self, item: typing.Union[str, int]) -> Real:
        if hasattr(item, '__index__'):
            item = item.__index__()
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

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    def __eq__(self, other: VectorLike) -> bool:
        if is_vector_like(other):
            other = _mkvector(other)
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other: VectorLike) -> bool:
        if is_vector_like(other):
            other = _mkvector(other)
            return self.x != other.x or self.y != other.y
        else:
            return True

    def __iter__(self) -> typing.Iterator[Real]:
        yield self.x
        yield self.y

    def __neg__(self) -> 'Vector2':
        return self * -1

    def angle(self, other: VectorLike) -> Real:
        other = _mkvector(other, castto=Vector2)
        return degrees(acos(self.normalize() * other.normalize()))

    def isclose(self, other: 'Vector2', *, rel_tol: float=1e-06, abs_tol: float=1e-3):
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
        diff = (self - other).length
        return (
            diff < rel_tol * max(self.length, other.length) or 
            diff < abs_tol
        )

    def rotate(self, degrees: Real) -> 'Vector2':
        r = radians(degrees)
        r_cos = cos(r)
        r_sin = sin(r)
        x = self.x * r_cos - self.y * r_sin
        y = self.x * r_sin + self.y * r_cos
        return Vector2(x, y)

    def normalize(self) -> 'Vector2':
        return self.scale(1)

    def truncate(self, max_length: Real) -> 'Vector2':
        if self.length > max_length:
            return self.scale(max_length)
        return self

    def scale(self, length: Real) -> 'Vector2':
        try:
            scale = length / self.length
        except ZeroDivisionError:
            scale = 1
        return self * scale

    def reflect(self, surface_normal: VectorLike) -> 'Vector2':
        """
        Calculate the reflection of the vector against a given surface normal
        """
        surface_normal = _mkvector(surface_normal, castto=Vector2)
        if not (0.99999 < surface_normal.length < 1.00001):
            raise ValueError("Reflection requires a normalized vector.")
        vec_new = self
        if self * surface_normal > 0:
            vec_new = self.rotate(180)
        return vec_new - (2 * (vec_new * surface_normal) * surface_normal)
