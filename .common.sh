set -euo pipefail

function run() {
    echo '$' "$@"
    "$@"
    echo
}

function die() {
    echo "$@" >&2
    exit 1
}

PY=${PY-python3}

command -v $PY >/dev/null || die "Python interpreter '$PY' not found"

PY_MAJOR="$($PY -c 'import sys; print(sys.version_info.major)')"
PY_MINOR="$($PY -c 'import sys; print(sys.version_info.minor)')"

[ "${PY_MAJOR}" -eq 3 ] || die Only Python 3 is supported
