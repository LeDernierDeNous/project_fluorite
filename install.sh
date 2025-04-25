#!/bin/bash

# Project Fluorite Install Script
set -e

echo "🔵 Starting Project Fluorite Setup..."

# Check for basic tools
REQUIRED_PKGS=("python3" "python3-venv" "python3-pip" "glxinfo")
for PKG in "${REQUIRED_PKGS[@]}"; do
    if ! command -v "$PKG" &> /dev/null; then
        echo "🛑 Missing required package: $PKG"
        echo "➡️ Installing missing system packages..."
        sudo apt update
        sudo apt install -y python3 python3-venv python3-pip mesa-utils
        break
    fi
done

# Check OpenGL version
GL_VERSION=$(glxinfo | grep "OpenGL version string" | awk '{print $4}' | cut -d'.' -f1)
if [ "$GL_VERSION" -lt 3 ]; then
    echo "🛑 OpenGL version $GL_VERSION detected! Minimum required: 3.0"
    echo "❌ Please update your GPU drivers and Mesa libraries."
    exit 1
else
    echo "✅ OpenGL $GL_VERSION detected. Good to go!"
fi

# Set up venv
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install all Python dependencies from requirements.txt
echo "📚 Installing Python libraries..."
pip install -r requirements.txt

echo "✅ Project Fluorite Installation Finished!"
echo "👉 You can now start the game with ./start.sh"