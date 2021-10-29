#!/usr/bin/env python3
import pyperf  # type: ignore

from ppb_vector import Vector
from utils import *


X = Vector(1, 1)
Y = Vector(0, 1)
λ = 123


def benches(r: pyperf.Runner):
   for f in BINARY_OPS + BINARY_SCALAR_OPS + BOOL_OPS:  # type: ignore
        r.bench_func(f.__name__, f, X, Y)

    for f in UNARY_OPS + UNARY_SCALAR_OPS:  # type: ignore
        r.bench_func(f.__name__, f, X)

    for f in SCALAR_OPS:  # type: ignore
        r.bench_func(f.__name__, f, X, λ)  # type: ignore


if __name__ == "__main__":
    r = pyperf.Runner()
    benches(r)
