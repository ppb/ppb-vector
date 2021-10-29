#!/usr/bin/env python3
from pathlib import Path
from sys import argv
from typing import List, Optional
from warnings import warn

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


def is_git_clean() -> bool:
    from dulwich import porcelain
    s = porcelain.status()

    # Deliberately ignoring untracked files
    return not (s.unstaged or any(s.staged.values()))


def git_version() -> Optional[str]:
    try:
        from dulwich.repo import Repo
    except ImportError:
        warn("dulwich unavailable, not saving bench data by default.")
        return None

    if not is_git_clean():
        return None
    
    # Extract the “short hash” for HEAD
    return Repo('.').head()[:7].decode('ASCII')


def bench_name(args: List[str] = argv) -> str:
    if '--fast' in args:
        return 'fast'
    elif '--rigorous' in args:
        return 'rigorous'
    else:
        return 'std'


if __name__ == "__main__":
    v = git_version()
    if v is not None and '--worker' not in argv:
        n = bench_name()
        p = Path(__file__).parent / 'benchdata'
        p.mkdir(exist_ok=True)
        argv.extend(('-o', str(p / f'{n}_bench_{v}.json')))

    r = pyperf.Runner()
    benches(r)
