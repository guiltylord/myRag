#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

PYTHON_BIN=${PYTHON_BIN:-python3}
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
OLLAMA_MODEL="phi3:mini"

echo "=== [1/3] Setting up virtualenv ==="
if [ ! -d "$VENV_DIR" ]; then
  $PYTHON_BIN -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "=== [2/3] Installing dependencies from $REQUIREMENTS_FILE ==="
if [ -f "$REQUIREMENTS_FILE" ]; then
  pip install --upgrade pip
  pip install -r "$REQUIREMENTS_FILE"
else
  echo "requirements.txt not found, skipping."
fi

echo "=== [3/3] Pulling Ollama model: $OLLAMA_MODEL ==="
if command -v ollama >/dev/null 2>&1; then
  ollama pull "$OLLAMA_MODEL"
else
  echo "WARNING: ollama not found in PATH. Install Ollama first and run this script again."
fi

echo "=== Done. To start the app: ==="
echo "source $VENV_DIR/bin/activate && python src/main.py"
