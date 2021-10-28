#!/usr/bin/env bash
source .common.sh

PYTEST_OPTIONS=()

if [[ "${CI+x}" == x ]]; then
		# Use a CI-specific profile for Hypothesis
		PYTEST_OPTIONS+=( --hypothesis-profile ci )

		# Autodetect the level of parallelism if unspecified
		PYTEST_OPTIONS+=( -n "${PYTEST_CPUS-auto}" )

elif ${PY} -m pip show -q pytest-xdist 2>/dev/null; then
		# Autoparallelise the testsuite when pytest-xdist is available
		PYTEST_OPTIONS=( -n auto )
fi

run ${PY} -m pytest "${PYTEST_OPTIONS[@]}" "$@"
