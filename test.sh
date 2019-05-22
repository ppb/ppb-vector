#!/usr/bin/env bash
source .common.sh

if [[ "${CI+x}" == x ]]; then
    IN_CI=1
    PYTEST_OPTIONS=( --hypothesis-profile ci )
else
    IN_CI=0
    PYTEST_OPTIONS=( )
fi


run ${PY} -m doctest README.md ppb_vector/__init__.py
run ${PY} -m pytest "${PYTEST_OPTIONS[@]}"
