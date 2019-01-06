#!/usr/bin/env bash
set -euxo pipefail

# Nothing to do if no specific Python version is requested
[ -n "${PYTHON+x}" ] || return 0

if [[ "$TRAVIS_OS_NAME" != linux ]]; then
   echo "This script only supports linux, got \$TRAVIS_OS_NAME='${TRAVIS_OS_NAME}'" >&2
   exit 1
fi

if [[ "$PYTHON" =~ pypy-* ]]; then
  # Download & install a prebuilt pypy snapshot
  PYPY_BRANCH=${PYTHON#*-}
  URL="http://buildbot.pypy.org/nightly/${PYPY_BRANCH}/pypy-c-jit-latest-linux64.tar.bz2"
  wget "${URL}" -O pypy.tar.bz2
  tar -xf pypy.tar.bz2
  PYPY=( pypy-c-jit-* )

  echo "Using ${PYPY}"
  export PATH="${PWD}/${PYPY}/bin:${PATH}"
  ln -s pypy3 "${PYPY}/bin/python"
  python -m ensurepip
  ln -s pip3 "${PYPY}/bin/pip"
  pip install -U pip wheel

else
  # Install a Python version with miniconda
  MINICONDA_OS=Linux
  URL="https://repo.continuum.io/miniconda/Miniconda3-latest-${MINICONDA_OS}-x86_64.sh"
  wget "${URL}" -O miniconda.sh
  bash miniconda.sh -b -p "$HOME/miniconda"
  export PATH="$HOME/miniconda/bin:$PATH"
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
  conda info -a
  conda create -q -n test-environment "python=$PYTHON"
  source activate test-environment
fi
