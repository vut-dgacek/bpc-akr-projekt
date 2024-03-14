#!/usr/bin/env bash
set -e
set -u

CWD="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
PATH="$CWD/.venv/bin:$PATH"

python "$CWD/src/client.py" "$@"
exit $?

