#!/usr/bin/env bash

# Nothing to do if no specific Python version is requested
[ -n "${PYTHON+x}" ] || return 0

function run() {
   echo '$' "$@"
   "$@" || exit 1
}

if [[ "$TRAVIS_OS_NAME" != linux ]]; then
   echo "This script only supports linux, got \$TRAVIS_OS_NAME='${TRAVIS_OS_NAME}'" >&2
   exit 1
fi

if [[ "$PYTHON" =~ pypy-* ]]; then
  # Download & install a prebuilt pypy snapshot
  PYPY_BRANCH=${PYTHON#*-}
  URL="http://buildbot.pypy.org/nightly/${PYPY_BRANCH}/pypy-c-jit-latest-linux64.tar.bz2"
  run wget "${URL}" -O ../pypy.tar.bz2
  run tar -C .. -xf ../pypy.tar.bz2
  pushd ..; PYPY=( pypy-c-jit-* ); popd

  echo "Using ${PYPY}"
  export PATH="$(realpath ../${PYPY}/bin):${PATH}"
  echo "PATH='${PATH}'"

  run ln -s pypy3 "../${PYPY}/bin/python"
  run python -m ensurepip
  run ln -s pip3 "../${PYPY}/bin/pip"

else
  # Install a Python version with miniconda
  MINICONDA_OS=Linux
  URL="https://repo.continuum.io/miniconda/Miniconda3-latest-${MINICONDA_OS}-x86_64.sh"
  run wget "${URL}" -O ../miniconda.sh
  run bash ../miniconda.sh -b -p "$HOME/miniconda"
  export PATH="$HOME/miniconda/bin:$PATH"
  echo "PATH='${PATH}'"

  run conda config --set always_yes yes --set changeps1 no
  run conda update -q conda
  run conda info -a
  run conda create -q -n test-environment "python=$PYTHON"
  run source activate test-environment
fi
