#!/usr/bin/env bash
source .common.sh

if [[ -v TRAVIS_OS_NAME ]] || [[ -v CI ]]; then
    IN_CI=1
    PYTEST_OPTIONS=( --hypothesis-profile ci )
else
    IN_CI=0
    PYTEST_OPTIONS=( )
fi


run ${PY} -m doctest README.md
run ${PY} -m pytest "${PYTEST_OPTIONS[@]}"
