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

