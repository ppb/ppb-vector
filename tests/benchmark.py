#!/usr/bin/env python3
import pyperf  # type: ignore

from ppb_vector import Vector
from utils import *

r = pyperf.Runner()
x = Vector(1, 1)
y = Vector(0, 1)
scalar = 123

for f in BINARY_OPS | BINARY_SCALAR_OPS | BOOL_OPS:  # type: ignore
    r.bench_func(f.__name__, f, x, y)

for f in UNARY_OPS | UNARY_SCALAR_OPS:  # type: ignore
    r.bench_func(f.__name__, f, x)

for f in SCALAR_OPS:  # type: ignore
    r.bench_func(f.__name__, f, x, scalar)  # type: ignore
