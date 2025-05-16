#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}                      OLLAMA-ANEKI-KITTY SETUP                                ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check if we're running in Kitty terminal
if ! command -v kitty &> /dev/null && [ "$TERM" != "xterm-kitty" ]; then
    echo -e "${RED}Warning: This script is designed for Kitty terminal which supports icat.${NC}"
    echo -e "${RED}Some features may not work correctly without Kitty terminal.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Setup aborted.${NC}"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Make sure python3-venv is installed.${NC}"
        echo -e "${YELLOW}Try: sudo apt install python3-venv${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${GREEN}Installing required packages...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${GREEN}Creating necessary directories...${NC}"
mkdir -p saves/custom/models
mkdir -p saves/custom/exp
mkdir -p saves/default

# Copy config if it doesn't exist yet
if [ ! -f "saves/default/config.conf" ]; then
    echo -e "${GREEN}Copying default configuration...${NC}"
    cp config.conf saves/default/config.conf
else
    echo -e "${GREEN}Configuration file already exists.${NC}"
fi

# Create alias in .bashrc if it doesn't exist
ALIAS_LINE="alias aneki='cd $(pwd) && source venv/bin/activate && python run.py'"
if ! grep -q "alias aneki=" ~/.bashrc; then
    echo -e "${GREEN}Adding alias to .bashrc...${NC}"
    echo "$ALIAS_LINE" >> ~/.bashrc
    echo -e "${YELLOW}Alias added to .bashrc. You'll need to run 'source ~/.bashrc' or restart your terminal.${NC}"
else
    echo -e "${GREEN}Alias already exists in .bashrc.${NC}"
fi

# Create alias in .zshrc if zsh is installed
if command -v zsh &> /dev/null; then
    if [ -f ~/.zshrc ] && ! grep -q "alias aneki=" ~/.zshrc; then
        echo -e "${GREEN}Adding alias to .zshrc...${NC}"
        echo "$ALIAS_LINE" >> ~/.zshrc
        echo -e "${YELLOW}Alias added to .zshrc. You'll need to run 'source ~/.zshrc' or restart your terminal.${NC}"
    elif [ -f ~/.zshrc ]; then
        echo -e "${GREEN}Alias already exists in .zshrc.${NC}"
    fi
fi

# Make run.py executable
chmod +x run.py

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${YELLOW}To use Ollama-Aneki-Kitty, run one of the following:${NC}"
echo -e "${BLUE}1. Source your terminal configuration:${NC}"
echo -e "   ${GREEN}source ~/.bashrc${NC} (for bash)"
echo -e "   ${GREEN}source ~/.zshrc${NC} (for zsh)"
echo -e "${BLUE}2. Then, you can use the 'aneki' command from anywhere:${NC}"
echo -e "   ${GREEN}aneki${NC} - for the main interface"
echo -e "   ${GREEN}aneki run [model_name]${NC} - to run a specific model"
echo -e "   ${GREEN}aneki new${NC} - to create a new model"
echo -e "   ${GREEN}aneki history${NC} - to view model history"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"