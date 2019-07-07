import typing
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import atan2, copysign, cos, degrees, hypot, isclose, radians, sin, sqrt

__all__ = ('Vector',)

#: ppb_vector's current version.
#: It follows the semantic versioning convention.
__version__ = "1.0"


# Anything convertable to a Vector, including lists, tuples, and dicts
VectorLike = typing.Union[
    'Vector',  # Or subclasses, unconnected to the Vector typevar above
    typing.Tuple[typing.SupportsFloat, typing.SupportsFloat],
    typing.Sequence[typing.SupportsFloat],  # TODO: Length 2
    typing.Mapping[str, typing.SupportsFloat],  # TODO: Length 2, keys 'x', 'y'
]


@dataclass(eq=False, frozen=True, init=False, repr=False)
class Vector:
    """The immutable, 2D vector class of the PursuedPyBear project.

    :py:class:`Vector` is an immutable 2D Vector, which can be instantiated as
    expected:

    >>> from ppb_vector import Vector
    >>> Vector(3, 4)
    Vector(3.0, 4.0)

    :py:class:`Vector` implements many convenience features, as well as
    useful mathematical operations for 2D geometry and linear algebra.

    :py:class:`Vector` acts as an iterable and a sequence, allowing usage like
    converting, indexing, and unpacking:

    >>> v = Vector(-3, -5)
    >>> list(v)
    [-3.0, -5.0]
    >>> tuple(v)
    (-3.0, -5.0)

    >>> v[0]
    -3.0

    >>> x, y = Vector(1, 2)
    >>> x
    1.0

    >>> print( *Vector(1, 2) )
    1.0 2.0

    It also acts mostly like a mapping, when it does not conflict with being a
    sequence. In particular, the coordinates may be accessed by subscripting:

    >>> v["y"]
    -5.0
    >>> v["x"]
    -3.0
    """
    x: float
    y: float

    # Tell CPython that this isn't an extendable dict
    __slots__ = ('x', 'y', '__weakref__')

    @typing.overload
    def __new__(cls, x: typing.SupportsFloat, y: typing.SupportsFloat): pass

    @typing.overload
    def __new__(cls, other: VectorLike): pass

    def __new__(cls, *args, **kwargs):
        """
        Make a vector from coordinates, or convert a vector-like.

        A vector-like can be:

        - a length-2 :py:class:`Sequence <collections.abc.Sequence>`, whose
          contents are interpreted as the ``x`` and ``y`` coordinates like ``(4, 2)``

        - a length-2 :py:class:`Mapping <collections.abc.Mapping>`, whose keys
          are ``x`` and ``y`` like ``{'x': 4, 'y': 2}``

        - any instance of :py:class:`Vector` or any subclass.
        """
        if args and kwargs:
            raise TypeError("Got a mix of positional and keyword arguments")

        if not args and not kwargs or len(args) > 2:
            raise TypeError("Expected 1 vector-like or 2 float-like arguments, "
                            f"got {len(args) + len(kwargs)}")

        if kwargs and frozenset(kwargs) != {'x', 'y'}:
            raise TypeError(f"Expected keyword arguments x and y, got: {kwargs.keys().join(', ')}")

        if kwargs:
            x, y = kwargs['x'], kwargs['y']
        elif len(args) == 1:
            value = args[0]
            if isinstance(value, cls):
                # Short circuit if already a valid instance
                return value

            x, y = Vector._unpack(value)
        elif len(args) == 2:
            x, y = args

        self = super().__new__(cls)

        try:
            # The @dataclass decorator made the class frozen, so we need to
            #  bypass the class' default assignment function :
            #
            #  https://docs.python.org/3/library/dataclasses.html#frozen-instances
            object.__setattr__(self, 'x', float(x))
        except ValueError:
            raise TypeError(f"{type(x).__name__} object not convertable to float")

        try:
            object.__setattr__(self, 'y', float(y))
        except ValueError:
            raise TypeError(f"{type(y).__name__} object not convertable to float")

        return self

    def __reduce__(self):
        return Vector, (self.x, self.y)

    def update(self,
               x: typing.Optional[typing.SupportsFloat] = None,
               y: typing.Optional[typing.SupportsFloat] = None):
        """Return a new :py:class:`Vector` replacing specified fields with new values."""
        if x is None and y is None:
            return self

        return Vector(self.x if x is None else x,
                      self.y if y is None else y)

    @staticmethod
    def _unpack(value: VectorLike) -> typing.Tuple[float, float]:
        if isinstance(value, Vector):
            return value.x, value.y
        elif isinstance(value, Sequence) and len(value) == 2:
            return float(value[0]), float(value[1])
        elif isinstance(value, Mapping) and 'x' in value and 'y' in value and len(value) == 2:
            return float(value['x']), float(value['y'])
        else:
            raise ValueError(f"Cannot use {value} as a vector-like")

    def __bool__(self) -> bool:
        """Check whether the vector is non-zero.

        >>> assert Vector(1, 1)
        >>> assert not Vector(0, 0)
        """
        return self != (0, 0)

    @property
    def length(self) -> float:
        """Compute the length of a vector.

        >>> Vector(45, 60).length
        75.0
        """
        # Surprisingly, caching this value provides no descernable performance
        # benefit, according to microbenchmarks.
        return hypot(self.x, self.y)

    def asdict(self) -> typing.Mapping[str, float]:
        """Convert a vector to a vector-like dictionary.

        >>> v = Vector(42, 69)
        >>> v.asdict()
        {'x': 42.0, 'y': 69.0}

        The conversion can be reversed by constructing:

        >>> assert v == Vector(v.asdict())
        """
        return {'x': self.x, 'y': self.y}

    def __len__(self) -> int:
        return 2

    def __add__(self, other: VectorLike) -> 'Vector':
        """Add two vectors.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> Vector(1, 0) + (0, 1)
        Vector(1.0, 1.0)
        >>> (0, 1) + Vector(1, 0)
        Vector(1.0, 1.0)
        """
        try:
            other_x, other_y = Vector._unpack(other)
        except ValueError:
            return NotImplemented

        return Vector(self.x + other_x, self.y + other_y)

    def __radd__(self, other: VectorLike) -> 'Vector':
        return self + other

    def __sub__(self, other: VectorLike) -> 'Vector':
        """Subtract one vector from another.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> Vector(3, 3) - (1, 1)
        Vector(2.0, 2.0)
        """
        try:
            other_x, other_y = Vector._unpack(other)
        except ValueError:
            return NotImplemented

        return Vector(self.x - other_x, self.y - other_y)

    def dot(self, other: VectorLike) -> float:
        """Compute the dot product of two vectors.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> Vector(1, 1).dot((-1, -1))
        -2.0

        This can also be expressed with :py:meth:`* <__mul__>`:

        >>> assert Vector(1, 2).dot([2, 1]) == Vector(1, 2) * [2, 1]
        """
        other_x, other_y = Vector._unpack(other)
        return self.x * other_x + self.y * other_y

    def scale_by(self, scalar: typing.SupportsFloat) -> 'Vector':
        """Compute a vector-scalar multiplication.

        >>> Vector(1, 2).scale_by(3)
        Vector(3.0, 6.0)

        Can also be expressed with :py:meth:`* <__mul__>`:

        >>> assert Vector(1, 2).scale_by(3) == 3 * Vector(1, 2)
        """
        scalar = float(scalar)
        return Vector(scalar * self.x, scalar * self.y)

    @typing.overload
    def __mul__(self, other: VectorLike) -> float: pass

    @typing.overload
    def __mul__(self, other: typing.SupportsFloat) -> 'Vector': pass

    def __mul__(self, other):
        """Perform a dot product or a scalar product, based on the parameter type.

        :param other: If ``other`` is a scalar (an instance of
          :py:class:`typing.SupportsFloat`), return
          :py:meth:`self.scale_by(other) <scale_by>`.

           >>> v = Vector(1, 1)
           >>> 3 * v
           Vector(3.0, 3.0)

           >>> assert 3 * v == v * 3 == v.scale_by(3)

          A :py:class:`Vector` can also be divided by a scalar,
            using the :py:meth:`/ <__truediv__>` operator:

           >>> assert 3 * v / 3 == v

        :param other: If ``other`` is a vector-like, return
          :py:meth:`self.dot(other) <dot>`.

          >>> v * (-1, -1)
          -2.0

          >>> assert v * (-1, -1) == (-1, -1) * v == v.dot((-1, -1))

          Vector-likes are defined in :py:meth:`convert`.
        """
        if isinstance(other, (float, int)):
            return self.scale_by(other)

        try:
            return self.dot(other)
        except (TypeError, ValueError):
            return NotImplemented

    @typing.overload
    def __rmul__(self, other: VectorLike) -> float: pass

    @typing.overload
    def __rmul__(self, other: typing.SupportsFloat) -> 'Vector': pass

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: typing.SupportsFloat) -> 'Vector':
        """Perform a division between a vector and a scalar.

        >>> Vector(3, 3) / 3
        Vector(1.0, 1.0)
        """
        other = float(other)
        return Vector(self.x / other, self.y / other)

    def __getitem__(self, item: typing.Union[str, int]) -> float:
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

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other: typing.Any) -> bool:
        """Test wheter two vectors are equal.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> Vector(1, 0) == (0, 1)
        False
        """
        try:
            other_x, other_y = Vector._unpack(other)
        except (TypeError, ValueError):
            return NotImplemented
        else:
            return self.x == other_x and self.y == other_y

    def __iter__(self) -> typing.Iterator[float]:
        yield self.x
        yield self.y

    def __neg__(self) -> 'Vector':
        """Negate a vector.

        Negating a :py:class:`Vector` produces one with identical length and opposite
        direction. It is equivalent to multiplying it by -1.

        >>> -Vector(1, 1)
        Vector(-1.0, -1.0)
        """
        return self.scale_by(-1)

    def angle(self, other: VectorLike) -> float:
        """Compute the angle between two vectors.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> Vector(1, 0).angle( (0, 1) )
        90.0

        As with :py:meth:`rotate`, angles are expressed in degrees, signed, and
        refer to a direct coordinate system (i.e. positive rotations are
        counter-clockwise).

        :py:meth:`angle` is guaranteed to produce an angle between -180° and 180°.
        """
        other_x, other_y = Vector._unpack(other)

        rv = degrees(atan2(other_x, -other_y) - atan2(self.x, -self.y))
        # This normalizes the value to (-180, +180], which is the opposite of
        # what Python usually does but is normal for angles
        if rv <= -180:
            rv += 360
        elif rv > 180:
            rv -= 360

        return rv

    def isclose(self, other: VectorLike, *,
                abs_tol: typing.SupportsFloat = 1e-09, rel_tol: typing.SupportsFloat = 1e-09,
                rel_to: typing.Sequence[VectorLike] = ()) -> bool:
        """Perform an approximate comparison of two vectors.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        >>> assert Vector(1, 0).isclose((1, 1e-10))

        :py:meth:`isclose` takes optional, keyword arguments, akin to those of
        :py:func:`math.isclose`:

        :param abs_tol: the absolute tolerance is the minimum magnitude (of the
            difference vector) under which two inputs are considered close,
            without consideration for (the magnitude of) the input values.

        :param rel_tol: the relative tolerance: if the length of the difference
            vector is less than ``rel_tol * input.length`` for any ``input``, the
            two vectors are considered close.

        :param rel_to: an iterable of additional vector-likes which are
            considered to be inputs, for the purpose of the relative tolerance.
        """
        abs_tol, rel_tol = float(abs_tol), float(rel_tol)
        if abs_tol < 0 or rel_tol < 0:
            raise ValueError("Vector.isclose takes non-negative tolerances")

        other = Vector(other)

        rel_length = max(
            self.length,
            other.length,
            *map(lambda v: Vector(v).length, rel_to),
        )

        diff = (self - other).length
        return (diff <= rel_tol * rel_length or diff <= float(abs_tol))

    @staticmethod
    def _trig(angle: typing.SupportsFloat) -> typing.Tuple[float, float]:
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

    def rotate(self, angle: typing.SupportsFloat) -> 'Vector':
        """Rotate a vector.

        Rotate a vector in relation to the origin and return a new :py:class:`Vector`.

        >>> Vector(1, 0).rotate(90)
        Vector(0.0, 1.0)

        Positive rotation is counter/anti-clockwise.
        """
        r_cos, r_sin = Vector._trig(angle)

        x = self.x * r_cos - self.y * r_sin
        y = self.x * r_sin + self.y * r_cos
        return Vector(x, y)

    def normalize(self) -> 'Vector':
        """Return a vector with the same direction and unit length.

        >>> Vector(3, 4).normalize()
        Vector(0.6, 0.8)

        Note that :py:meth:`normalize()` is equivalent to :py:meth:`scale(1) <scale>`:

        >>> assert Vector(7, 24).normalize() == Vector(7, 24).scale_to(1)
        """
        return self.scale(1)

    def truncate(self, max_length: typing.SupportsFloat) -> 'Vector':
        """Scale a given :py:class:`Vector` down to a given length, if it is larger.

        >>> Vector(7, 24).truncate(3)
        Vector(0.84, 2.88)

        It produces a vector with the same direction, but possibly a different
        length.

        Note that :py:meth:`vector.scale(max_length) <scale>` is equivalent to
        :py:meth:`vector.truncate(max_length) <truncate>` when
        :py:meth:`max_length ≨ vector.length <length>`.

        >>> Vector(3, 4).scale(4)
        Vector(2.4, 3.2)
        >>> Vector(3, 4).truncate(4)
        Vector(2.4, 3.2)

        >>> Vector(3, 4).scale(6)
        Vector(3.6, 4.8)
        >>> Vector(3, 4).truncate(6)
        Vector(3.0, 4.0)

        Note: :py:meth:`x.truncate(max_length) <truncate>` may sometimes be
        slightly-larger than ``max_length``, due to floating-point rounding
        effects.
        """
        max_length = float(max_length)
        if self.length <= max_length:
            return self

        return self.scale_to(max_length)

    def scale_to(self, length: typing.SupportsFloat) -> 'Vector':
        """Scale a given :py:class:`Vector` to a certain length.

        >>> Vector(7, 24).scale_to(2)
        Vector(0.56, 1.92)
        """
        length = float(length)
        if length < 0:
            raise ValueError("Vector.scale_to takes non-negative lengths.")

        if length == 0:
            return Vector(0, 0)

        return (length * self) / self.length

    scale = scale_to

    def reflect(self, surface_normal: VectorLike) -> 'Vector':
        """Reflect a vector against a surface.

        :param other: A :py:class:`Vector` or a vector-like.
          For a description of vector-likes, see :py:func:`__new__`.

        Compute the reflection of a :py:class:`Vector` on a surface going
        through the origin, described by its normal vector.

        >>> Vector(5, 3).reflect( (-1, 0) )
        Vector(-5.0, 3.0)

        >>> Vector(5, 3).reflect( Vector(-1, -2).normalize() )
        Vector(0.5999999999999996, -5.800000000000001)
        """
        surface_normal = Vector(surface_normal)
        if not isclose(surface_normal.length, 1):
            raise ValueError("Reflection requires a normalized vector.")

        return self - (2 * (self * surface_normal) * surface_normal)


Sequence.register(Vector)
