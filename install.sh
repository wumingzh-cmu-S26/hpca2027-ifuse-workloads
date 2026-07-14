#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
venv="$root/.venv"

if [[ ! -x "$venv/bin/python" ]]; then
  python3 -m venv "$venv"
fi
"$venv/bin/python" -m pip install -q -r "$root/requirements.txt"
exec "$venv/bin/python" "$root/install_workloads.py" "$@"
