@echo off
cd /d "%~dp0"

echo [INFO] Starting ollama serve in separate window...
start "Ollama Server" cmd /k "ollama serve"

timeout /t 3 /nobreak >nul

call .venv\Scripts\activate
echo [INFO] Starting main.py...
echo ---------------------------------------
python src\main.py
echo ---------------------------------------
echo [DONE] Program finished.
pause
