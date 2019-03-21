set -euo pipefail

function run() {
    echo '$' "$@"
    "$@"
    echo
}

if [[ ! -v PY ]]; then
    PY=python3
fi

if ! command -v $PY >/dev/null; then
    echo "Python interpreter '$PY' not found" >&2
    exit 1
fi
