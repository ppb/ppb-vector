# ppb-vector
The immutable, 2D vector class for the PursuedPyBear project.

`Vector` implements many convenience features, as well as
useful mathematical operations for 2D geometry.

## Install

You can install `Vector` pip package using

```bash
pip install 'ppb-vector'
```

## Usage

`Vector` is an immutable 2D Vector, which is instantiated as expected: 

    >>> from ppb_vector import Vector
    >>> Vector(3, 4)
    Vector(3.0, 4.0)


See the [API reference] for an overview of the functionality.

Version numbers follow the [semantic versioning] convention, so [requiring]
`ppb-vector ~= 1.0` is appropriate for software developped against this release:
the version specification will match any 1.x release, starting with 1.0.

[API reference]: https://ppb-vector.readthedocs.io/en/latest/
[semantic versioning]: https://semver.org
[requiring]: https://www.python.org/dev/peps/pep-0508/
