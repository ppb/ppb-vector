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


Inheriting from :py:class:`Vector`
-----------------------------------

:py:class:`Vector` does not support inheritance.
