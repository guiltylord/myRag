@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
echo [INFO] Starting main.py...
echo ---------------------------------------
python main.py
echo ---------------------------------------
echo [DONE] Program finished.
pause