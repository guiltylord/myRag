#!/bin/bash
cd "$(dirname "$0")"

C_RESET='\033[0m'
C_RED='\033[31m'
C_GREEN='\033[32m'
C_YELLOW='\033[33m'
C_CYAN='\033[36m'
BRIGHT_YELLOW='\033[33;1m'

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
OLLAMA_MODEL="phi3:mini"
MAIN_PACKAGE="langchain"

clear
echo -e "${BRIGHT_YELLOW}                  oo dP   dP            dP                         dP ${C_RESET}"
echo -e "${BRIGHT_YELLOW}                     88   88            88                         88 ${C_RESET}"
echo -e "${BRIGHT_YELLOW}.d8888b. dP    dP dP 88 d8888P dP    dP 88 .d8888b. 88d888b. .d888b88 ${C_RESET}"
echo -e "${BRIGHT_YELLOW}88'  \`88 88    88 88 88   88   88    88 88 88'  \`88 88'  \`88 88'  \`88 ${C_RESET}"
echo -e "${BRIGHT_YELLOW}88.  .88 88.  .88 88 88   88   88.  .88 88 88.  .88 88       88.  .88 ${C_RESET}"
echo -e "${BRIGHT_YELLOW}\`8888P88 \`88888P' dP dP   dP   \`8888P88 dP \`88888P' dP       \`88888P8 ${C_RESET}"
echo -e "${BRIGHT_YELLOW}     .88                            .88                               ${C_RESET}"
echo -e "${BRIGHT_YELLOW} d8888P                         d8888P                                ${C_RESET}"
echo ""
echo -e "${C_CYAN}==========================================${C_RESET}"
echo -e "${C_CYAN}       RAG SYSTEM LAUNCHER (STABLE)       ${C_RESET}"
echo -e "${C_CYAN}==========================================${C_RESET}"
echo ""

if [ -f "${VENV_DIR}/bin/python" ]; then
    echo -e "${C_GREEN}[OK] Virtual environment found.${C_RESET}"
else
    echo -e "${C_YELLOW}[..] Creating virtual environment...${C_RESET}"
    python3 -m venv "${VENV_DIR}"
    if [ $? -ne 0 ]; then
        echo -e "${C_RED}[ERROR] Failed to create venv.${C_RESET}"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

source "${VENV_DIR}/bin/activate"

if python -c "import ${MAIN_PACKAGE}" >/dev/null 2>&1; then
    echo -e "${C_GREEN}[OK] Dependencies ready. Skipping pip install.${C_RESET}"
else
    echo -e "${C_YELLOW}[..] Installing dependencies...${C_RESET}"
    python -m pip install --upgrade pip --quiet
    if [ -f "${REQUIREMENTS_FILE}" ]; then
        python -m pip install -r "${REQUIREMENTS_FILE}"
        if [ $? -ne 0 ]; then
            echo -e "${C_RED}[ERROR] Pip install failed. Check requirements.txt!${C_RESET}"
            read -p "Press Enter to exit..."
            exit 1
        fi
    fi
fi

if ! command -v ollama &> /dev/null; then
    echo -e "${C_RED}[WARNING] Ollama not found in PATH!${C_RESET}"
else
    echo -e "${C_YELLOW}[..] Checking Ollama model '${OLLAMA_MODEL}'...${C_RESET}"
    ollama pull "${OLLAMA_MODEL}"
fi

read -p "Press Enter to continue..."