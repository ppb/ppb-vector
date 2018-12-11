# ppb-vector
The 2D Vector Class for the PursuedPyBear project.

## Install

You can install `Vector2` pip package using

```bash
pip install 'ppb-vector'
```

## Usage

`Vector2` is an immutable 2D Vector. Instantiated as expected: 

    >>>> from ppb_vector import Vector2
    >>> Vector2(3, 4)
    Vector2(3, 4)

`Vector2` implements many convenience features, as well as
useful mathematical operations for 2D geometry and linear algebra.


## Convenience functions

### Unpacking

    >>> x, y = Vector2(1, 3)
    >>> print(x)
    1
    >>> print(y)
    3
    
### Access Values

Convenient access to `Vector2` members via dot notation, indexes, or keys.

    >>> my_vector = Vector2(2, 3)
    >>> my_vector.x
    2
    >>> my_vector[1]
    3
    >>> my_vector["x"]
    2

Also iterable for translation between Vector2 and other sequence types.

    >>> tuple(Vector(2, 3))
    (2, 3)


## Mathematical operators

### Addition

    >>> Vector2(1, 0) + Vector2(0, 1)
    Vector2(1, 1)

In addition to `Vector2` addition also accepts vector-like objects such as
`tuple`, `list`, and `dict`.

    >>> Vector2(1, 1) + [1, 3]
    Vector2(2, 4)

    >>> Vector2(1, 1) + (2, 4)
    Vector2(3, 5)

    >>> Vector2(1, 1) + {"x": 3, "y": 5}
    Vector2(4, 6)

### Subtraction

    >>> Vector2(3, 3) - Vector2(1, 1)
    Vector2(2, 2)

As with addition, subtraction also takes vector-like objects.

    >>> Vector2(3, 3) - [2, 1]
    Vector2(1, 2)
    
    >>> Vector2(3, 3) - (2, 1)
    Vector2(1, 2)
    
    >>> Vector2(3, 3) - {"x": 2, "y": 1}
    Vector2(1, 2)


### Equality

Vectors are equal if their coordinates are equal.

    >>> Vector2(1, 0) == Vector2(0, 1)
    False

### Scalar Multiplication

Multiply a `Vector2` by a scalar to get a scaled `Vector2`:

    >>> 3 * Vector2(1, 1)
    Vector2(3, 3)

    >>> Vector2(1, 1) * 3
    Vector2(3, 3)

    >>> Vector2(1, 1).scale_by(3)
    Vector2(3, 3)

### Dot Product

Multiply a `Vector2` by another `Vector2` to get the dot product.

    >>> Vector2(1, 1) * Vector2(-1, -1)
    -2

### Vector Length

    >>> Vector2(45, 60).length
    75.0

### Cross-product

Take the cross-product between two (2D) vectors.
The result is expressed as a scalar, as it is known to lie on the z-axis.

    >>> Vector(1, 0) ^ Vector(0, 1)
    1

### Negation

Negating a `Vector2` is equivalent to multiplying it by -1.

    >>> -Vector2(1, 1)
    Vector2(-1.0, -1.0)


## Methods

Useful functions for game development.

### isclose(vector)

Perform an approximate comparison of two vectors.

    >>> Vector2(1, 0).isclose((1, 1e-10))
    True

`Vector2.isclose` takes optional, keyword arguments, akin to those of
`math.isclose`:
- `abs_tol` (absolute tolerance) is the minimum magnitude (of the difference
  vector) under which two inputs are considered close, without consideration for
  (the magnitude of) the input values.
- `rel_tol` (relative tolerance) is the relative error: if the length of the
  difference vector is less than `rel_tol * input.length` for any `input`,
  the two vectors are considered close.
- `rel_to` is an iterable of additional vector-likes whose length (times
  `rel_tol`) is compared to the length of the difference vector.

By default, `abs_tol = 1e-3`, `rel_tol = 1e-6`, and `rel_to = []`.

### rotate(deg)

Rotate a vector in relation to its own origin and return a new `Vector2`.

    >>> Vector2(1, 0).rotate(90)
    Vector2(0.0, 1.0)

Positive rotation is counter/anti-clockwise.

### angle(vector)

Compute the angle between two vectors, expressed as a scalar in degrees.

    >>> Vector(1, 0).angle(Vector(0, 1))
    90

As with `rotate()`, angles are signed, and refer to a direct coordinate system
(i.e. positive rotations are counter-clockwise).

`Vector2.angle` is guaranteed to produce an angle between -180° and 180°.

### normalize()

Return a vector with the same direction, and unit length.

    >>> Vector2(5, 5).normalize()
    Vector2(0.7071067811865475, 0.7071067811865475)

### scale(scalar)

Scale given `Vector2` to a given length.

    >>> Vector2(7, 7).scale(5)
    Vector2(3.5355339059327373, 3.5355339059327373)

Note that `Vector2.normalize()` is equivalent to `Vector2.scale(1)`.

    >>> Vector2(200, 300).normalize()
    Vector2(0.5547001962252291, 0.8320502943378436)
    >>> Vector2(200, 300).scale(1)
    Vector2(0.5547001962252291, 0.8320502943378436)

### truncate(scalar)

Scale a given `Vector2` down to a given length, if it is larger.

    >>> Vector2(700, 500).truncate(5)
    Vector2(4.068667356033675, 2.906190968595482)

Note that `Vector2.scale` is equivalent to `Vector2.truncate` when `scalar` is
less than length.

    >>> Vector2(3, 4).scale(4)
    Vector2(2.4000000000000004, 3.2)
    >>> Vector2(3, 4).truncate(4)
    Vector2(2.4000000000000004, 3.2)
    >>> Vector2(3, 4).scale(6)
    Vector2(3.5999999999999996, 4.8)
    >>> Vector2(3, 4).truncate(6)
    Vector2(3, 4)

### reflect(surface_normal)

Reflect a `Vector2` based on a given surface normal.

    >>> Vector2(5, 3).reflect(Vector2(-1, 0))
    Vector2(-5, 3)
    >>> Vector2(5, 3).reflect(Vector2(-1, -2).normalize())
    Vector2(0.5999999999999996, -5.800000000000001)
