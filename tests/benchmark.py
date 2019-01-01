#!/usr/bin/env python3
import perf # type: ignore
from ppb_vector import Vector2
from utils import *

r = perf.Runner()
x = Vector2(1, 1)
y = Vector2(0, 1)
scalar = 123

for f in BINARY_OPS + BINARY_SCALAR_OPS + BOOL_OPS: # type: ignore
    r.bench_func(f.__name__, f, x, y)

for f in UNARY_OPS + UNARY_SCALAR_OPS: # type: ignore
    r.bench_func(f.__name__, f, x)

for f in SCALAR_OPS: # type: ignore
    r.bench_func(f.__name__, f, x, scalar)
