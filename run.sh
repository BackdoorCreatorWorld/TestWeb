#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[36m═══════════════════════════════════════════════\e[0m"
echo -e "\e[32m   ARCHITECT 01 - LOCAL WEB SERVER LAUNCHER   \e[0m"
echo -e "\e[36m═══════════════════════════════════════════════\e[0m"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "\e[31m❌ Python3 not found! Installing...\e[0m"
    pkg install python -y
fi

# Install requirements
echo -e "\e[33m📦 Installing requirements...\e[0m"
pip install flask flask-cors colorama psutil

# Create directories if not exist
mkdir -p templates static

# Check if files exist
if [ ! -f "templates/index.html" ]; then
    echo -e "\e[31m❌ templates/index.html not found!\e[0m"
    exit 1
fi

if [ ! -f "templates/blocked.html" ]; then
    echo -e "\e[31m❌ templates/blocked.html not found!\e[0m"
    exit 1
fi

# Run server
echo -e "\e[32m✅ Starting server...\e[0m"
python3 server.py
