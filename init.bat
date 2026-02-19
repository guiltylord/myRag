@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "PYTHON_BIN=python"
set "VENV_DIR=.venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "OLLAMA_MODEL=phi3:mini"

echo === [1/3] Setting up virtualenv ===
if not exist "%VENV_DIR%" (
    %PYTHON_BIN% -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate"

echo === [2/3] Installing dependencies from %REQUIREMENTS_FILE% ===
if exist "%REQUIREMENTS_FILE%" (
    python -m pip install --upgrade pip
    python -m pip install -r "%REQUIREMENTS_FILE%"
) else (
    echo requirements.txt not found, skipping.
)

echo === [3/3] Pulling Ollama model: %OLLAMA_MODEL% ===
where ollama >nul 2>nul
if %errorlevel%==0 (
    ollama pull %OLLAMA_MODEL%
) else (
    echo WARNING: ollama not found in PATH. Install Ollama first and run this script again.
)

echo === Done. To start the app: ===
echo call %VENV_DIR%\Scripts\activate ^&^& python src\main.py

endlocal
pause
