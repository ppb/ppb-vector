#!/usr/bin/env bash
source .common.sh

if [[ "${CI+x}" == x ]]; then
    IN_CI=1
    PYTEST_OPTIONS=( --hypothesis-profile ci )
else
    IN_CI=0
    PYTEST_OPTIONS=( )
fi

# Autoparallelise the testsuite when pytest-xdist is available
if ${PY} -m pip show -q pytest-xdist 2>/dev/null; then
    PYTEST_OPTIONS+=( -n auto )
fi

run ${PY} -m doctest README.md ppb_vector/__init__.py
run ${PY} -m pytest "${PYTEST_OPTIONS[@]}"
