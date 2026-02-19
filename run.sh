#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "[INFO] Starting main.py..."
echo "---------------------------------------"
python3 main.py
echo "---------------------------------------"
echo "[DONE] Program finished."
read -p "Press Enter to exit..."