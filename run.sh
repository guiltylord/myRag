#!/usr/bin/env bash
cd "$(dirname "$0")"

echo "[INFO] Starting ollama serve in separate terminal..."
gnome-terminal -- bash -c "ollama serve; exec bash"

sleep 3

source .venv/bin/activate
echo "[INFO] Starting main.py..."
echo "---------------------------------------"
python src/main.py
echo "---------------------------------------"
echo "[DONE] Program finished."
read -p "Press Enter to exit..."
