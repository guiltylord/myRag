@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%b"
set "C_RESET=%ESC%[0m"
set "C_RED=%ESC%[31m"
set "C_GREEN=%ESC%[32m"
set "C_YELLOW=%ESC%[33m"
set "C_CYAN=%ESC%[36m"

set "VENV_DIR=.venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "OLLAMA_MODEL=phi3:mini"
set "MAIN_PACKAGE=langchain"

cls
echo %C_CYAN%==========================================%C_RESET%
echo %C_CYAN%       RAG SYSTEM LAUNCHER (STABLE)       %C_RESET%
echo %C_CYAN%==========================================%C_RESET%
echo.

if exist "%VENV_DIR%\Scripts\python.exe" (
    echo %C_GREEN%[OK] Virtual environment found.%C_RESET%
) else (
    echo %C_YELLOW%[..] Creating virtual environment...%C_RESET%
    python -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        echo %C_RED%[ERROR] Failed to create venv.%C_RESET%
        pause
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate"

python -c "import %MAIN_PACKAGE%" >nul 2>&1
if !errorlevel! equ 0 (
    echo %C_GREEN%[OK] Dependencies ready. Skipping pip install.%C_RESET%
) else (
    echo %C_YELLOW%[..] Installing dependencies...%C_RESET%
    python -m pip install --upgrade pip --quiet
    if exist "%REQUIREMENTS_FILE%" (
        python -m pip install -r "%REQUIREMENTS_FILE%"
        if !errorlevel! neq 0 (
            echo %C_RED%[ERROR] Pip install failed. Check requirements.txt!%C_RESET%
            pause
            exit /b 1
        )
    )
)

where ollama >nul 2>nul
if !errorlevel! neq 0 (
    echo %C_RED%[WARNING] Ollama not found in PATH!%C_RESET%
) else (
    echo %C_YELLOW%[..] Checking Ollama model '%OLLAMA_MODEL%'...%C_RESET%
    ollama pull %OLLAMA_MODEL%
)

pause