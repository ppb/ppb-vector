#!/usr/bin/env bash
set -euo pipefail

function run() {
    echo '$' "$@"
    "$@"
    echo
}

if [[ -v TRAVIS_OS_NAME ]]; then
    IN_CI=1
    PYTEST_OPTIONS=( --hypothesis-profile ci )
else
    IN_CI=0
    PYTEST_OPTIONS=( )
fi

run pytest "${PYTEST_OPTIONS[@]}"
[[ "${PYTHON-x}" =~ pypy-* ]] || run mypy ppb_vector tests
run python -m doctest README.md
