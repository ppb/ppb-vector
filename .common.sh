set -euo pipefail

function run() {
    echo '$' "$@"
    "$@"
    echo
}
