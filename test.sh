#!/usr/bin/env bash
source .common.sh

if [[ -v TRAVIS_OS_NAME ]] || [[ -v CI ]]; then
    IN_CI=1
    PYTEST_OPTIONS=( --hypothesis-profile ci )
else
    IN_CI=0
    PYTEST_OPTIONS=( )
fi


run python -m doctest README.md
run pytest "${PYTEST_OPTIONS[@]}"
