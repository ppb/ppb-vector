#!/usr/bin/env bash
source .common.sh

if [[ "${PYTHON-x}" =~ pypy-* ]]; then
    echo "Skipping linting under pypy" >&2
    exit 0
fi

run flake8 --version
run flake8 --ignore E241,F403,F405,B011 tests
run flake8 --exclude tests/

# Exclusion due to https://github.com/python/mypy/pull/10191
run ${PY} -m mypy ppb_vector tests --exclude test_pattern_matching.py
