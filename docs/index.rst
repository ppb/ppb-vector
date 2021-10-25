PPB's 2D Vector class
=====================

.. note::
   ``ppb-vector`` follows the semver_ (semantic versioning) convention.
   In a nutshell, we commit to forward compatibility within a major version:
   code that works with version 1.0 ought to work with any 1.x release.

.. _semver: https://semver.org

.. autoclass:: ppb_vector.Vector
   :members:
   :special-members:
   :exclude-members: __init__, __radd__, __repr__, __weakref__, scale

    .. autoattribute:: x
        :annotation: : float
       
        The X coordinate of the vector

    .. autoattribute:: y
        :annotation: : float
       
        The Y coordinate of the vector


Pattern Matching
----------------

(Python 3.10 and up only. See pep636_ (PEP 636) for information on pattern
matching in general.)

:py:class:`Vector` supports not only basic pattern matching
(``case Vector(x=4, y=2):``), but also supports positional arguments
(``case Vector(4, 2):``) and also comparison to sequences
(``case (4, 2):``).

However, it does not support matching against dictionaries
(``case {'x': 4, 'y': 2}:``).

.. _pep636: https://www.python.org/dev/peps/pep-0636/


Inheriting from :py:class:`Vector`
-----------------------------------

:py:class:`Vector` does not support inheritance.
