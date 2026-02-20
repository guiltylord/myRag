@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%b"
set "C_RESET=%ESC%[0m"
set "C_RED=%ESC%[31m"
set "C_GREEN=%ESC%[32m"
set "C_YELLOW=%ESC%[33m"
set "C_CYAN=%ESC%[36m"

echo %C_YELLOW%[INFO] Starting ollama serve in separate window...%C_RESET%
start "Ollama Server" cmd /k "ollama serve"

timeout /t 3 /nobreak >nul

call .venv\Scripts\activate
echo %C_YELLOW%[INFO] Starting main.py...%C_RESET%
echo %C_CYAN%---------------------------------------%C_RESET%
python src\main.py
echo %C_CYAN%---------------------------------------%C_RESET%
echo %C_GREEN%[DONE] Program finished.%C_RESET%
pause