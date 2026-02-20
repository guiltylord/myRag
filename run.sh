#!/bin/bash
cd "$(dirname "$0")"

C_RESET='\033[0m'
C_RED='\033[31m'
C_GREEN='\033[32m'
C_YELLOW='\033[33m'
C_CYAN='\033[36m'
BRIGHT_YELLOW='\033[33;1m'

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

echo -e "${C_YELLOW}[INFO] Starting ollama serve in background...${C_RESET}"
ollama serve &

sleep 3

source .venv/bin/activate
echo -e "${C_YELLOW}[INFO] Starting main.py...${C_RESET}"
echo -e "${C_CYAN}---------------------------------------${C_RESET}"
python src/main.py
echo -e "${C_CYAN}---------------------------------------${C_RESET}"
echo -e "${C_GREEN}[DONE] Program finished.${C_RESET}"
read -p "Press Enter to exit..."