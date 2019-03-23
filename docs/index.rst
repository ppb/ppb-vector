PPB 2D Vector
=============

.. py:data:: ppb_vector.vector2.Vector
    :annotation: = typing.TypeVar('Vector', bound='Vector2')

    In the following, :py:data:`Vector` is a type variable that denotes either
    :py:class:`Vector2` or any of its subclasses. Implicitely, it is the type of
    ``self``--the type of the returned value will be the same subclass if called
    on a subclass


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
