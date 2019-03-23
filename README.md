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


See the [online documentation] for an overview of the functionality.

[online documentation]: https://ppb-vector.readthedocs.io/en/latest/


## Mathematical operators

In addition to `Vector2`s, operators also accept, as second operand,
vector-like objects such as `tuple`, `list`, and `dict`.

    >>> Vector2(1, 1) + [1, 3]
    Vector2(2.0, 4.0)

    >>> Vector2(1, 1) - (2, 4)
    Vector2(-1.0, -3.0)

    >>> Vector2(1, 1) * {"x": 3, "y": 5}
    8.0
