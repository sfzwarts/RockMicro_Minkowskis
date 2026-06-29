#!/usr/bin/env bash
set -euo pipefail

python_command="${PYTHON:-python3.12}"
venv_dir="${VENV_DIR:-.venv}"
install_target=".[dev]"
unpack_data=false

for argument in "$@"; do
  case "$argument" in
    --all) install_target=".[all,dev]" ;;
    --data) unpack_data=true ;;
    -h|--help)
      echo "Usage: ./setup.sh [--all] [--data]"
      echo "  --all   include Gmsh, PyVista, VTK, and TauFactor"
      echo "  --data  unpack archived coordinate data after installation"
      exit 0
      ;;
    *)
      echo "Unknown option: $argument" >&2
      exit 2
      ;;
  esac
done

if ! command -v "$python_command" >/dev/null 2>&1; then
  echo "Python 3.12 is required. Set PYTHON to a compatible interpreter." >&2
  exit 1
fi

"$python_command" -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install --upgrade pip
"$venv_dir/bin/python" -m pip install -e "$install_target"

if "$unpack_data"; then
  "$venv_dir/bin/python" tools/unpack_data.py
fi

echo "Environment ready. Activate it with: source $venv_dir/bin/activate"
