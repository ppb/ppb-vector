PPB's 2D Vector class
=====================

.. py:data:: ppb_vector.vector2.Vector
    :annotation: = typing.TypeVar('Vector', bound='Vector2')

    In the following, :py:data:`Vector` is a type variable (an instance of
    :py:class:`TypeVar <typing.TypeVar>`) that denotes either
    :py:class:`Vector2` or any of its subclasses. Implicitely, it is the type of
    ``self``: a method whose return type is :py:data:`Vector` will return a
    vector of the same type that it was called on.


.. autoclass:: ppb_vector.Vector2
   :members:
   :special-members:
   :exclude-members: __init__, __repr__, __weakref__, scale

    .. autoattribute:: x
        :annotation: : float
       
        The X coordinate of the vector

    .. autoattribute:: y
        :annotation: : float
       
        The Y coordinate of the vector


Inheriting from :py:class:`Vector2<ppb_vector.Vector2>`
-------------------------------------------------------

.. py:currentmodule:: ppb_vector

Subclasses that do not add attributes need not, and should not, define
:py:meth:`__init__<object.__init__>` or :py:meth:`__new__<object.__new__>`.

As :py:class:`Vector2` is a
:py:func:`dataclass<dataclasses.dataclass>` that implements
:py:meth:`__new__<object.__new__>`, subclasses that define additional attributes
should be frozen dataclasses, redefine :py:meth:`__new__<object.__new__>`, and
not define :py:meth:`__init__<object.__init__>`. The simplest way to do so looks
like so: ::

  @dataclass(frozen=True, init=False)
  class LabeledVector(Vector2):
      """Subclass of Vector2 that defines an additional attribute."""
      label: str
  
      def __new__(cls, x, y, label):
          self = super().__new__(cls, x, y)
          object.__setattr__(self, 'label', label)
          return self


Using :py:meth:`object.__setattr__` is necessary because the class is frozen by
the :py:func:`dataclass<dataclasses.dataclass>` decorator, and as such assigning
attributes raises an exception.

Some methods return another vector: binary operators
(:py:meth:`+<Vector2.__add__>`, :py:meth:`- <Vector2.__sub__>`,
:py:meth:`reflect<Vector2.reflect>`), scalar operators
(:py:meth:`rotate<Vector2.rotate>`, :py:meth:`scale_by<Vector2.scale_by>`,
:py:meth:`scale_to<Vector2.scale_to>`, :py:meth:`truncate<Vector2.truncate>`),
and unary operators (:py:meth:`-<Vector2.__neg__>`,
:py:meth:`normalize<Vector2.normalize>`). Those methods return an instance of
the subclass (see :py:data:`Vector<vector2.Vector>`), and preserve all
attributes of ``self`` except the cartesian coordinates (:py:attr:`x<Vector2.x>`
and :py:attr:`y<Vector2.y>`).
