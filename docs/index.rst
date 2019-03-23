.. ppb-vector documentation master file, created by
   sphinx-quickstart on Sat Mar 23 14:10:03 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ppb-vector's documentation!
======================================

.. py:data:: ppb_vector.vector2.Vector

In the following, :py:data:`Vector` is a type variable that denotes either
:py:class:`Vector2` or any of its subclasses. Implicitely, it is the type of
``self``.


.. autoclass:: ppb_vector.Vector2
   :members:
   :special-members:
   :exclude-members: __weakref__, __init__, scale

    .. autoattribute:: x
        :annotation: : float
       
        The X coordinate of the vector

    .. autoattribute:: y
        :annotation: : float
       
        The Y coordinate of the vector


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
