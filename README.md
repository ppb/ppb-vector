# ppb-vector
The immutable, 2D vector class for the PursuedPyBear project.

`Vector2` implements many convenience features, as well as
useful mathematical operations for 2D geometry.

## Install

You can install `Vector2` pip package using

```bash
pip install 'ppb-vector'
```

## Usage

`Vector2` is an immutable 2D Vector. Instantiated as expected: 

    >>> from ppb_vector import Vector2
    >>> Vector2(3, 4)
    Vector2(3.0, 4.0)



## Convenience functions

### Unpacking

    >>> x, y = Vector2(1, 3)
    >>> print(x)
    1.0
    >>> print(y)
    3.0
    
### Access Values

Convenient access to `Vector2` members via dot notation, indexes, or keys.

    >>> my_vector = Vector2(2, 3)
    >>> my_vector.x
    2.0
    >>> my_vector[1]
    3.0
    >>> my_vector["x"]
    2.0

Also iterable for translation between Vector2 and other sequence types.

    >>> tuple(Vector2(2, 3))
    (2.0, 3.0)


## Mathematical operators

In addition to `Vector2`s, operators also accept, as second operand,
vector-like objects such as `tuple`, `list`, and `dict`.

    >>> Vector2(1, 1) + [1, 3]
    Vector2(2.0, 4.0)

    >>> Vector2(1, 1) + (2, 4)
    Vector2(3.0, 5.0)

    >>> Vector2(1, 1) + {"x": 3, "y": 5}
    Vector2(4.0, 6.0)


### Scalar Multiplication

Multiply a `Vector2` by a scalar to get a scaled `Vector2`:

    >>> 3 * Vector2(1, 1)
    Vector2(3.0, 3.0)

    >>> Vector2(1, 1) * 3
    Vector2(3.0, 3.0)

    >>> Vector2(1, 1).scale_by(3)
    Vector2(3.0, 3.0)


It is also possible to divide a `Vector2` by a scalar:

    >>> Vector2(3, 3) / 3
    Vector2(1.0, 1.0)

### Dot Product

Multiply a `Vector2` by another `Vector2` to get the dot product.

    >>> Vector2(1, 1) * (-1, -1)
    -2.0

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
