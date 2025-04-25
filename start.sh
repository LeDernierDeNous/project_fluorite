#!/bin/bash

# Project Fluorite Start Script v3 (LD_PRELOAD + Anaconda clean fix)
set -e

echo "🎮 Starting the Game..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "🛑 Virtual environment not found! Run ./install.sh first."
    exit 1
fi

# If running inside Conda, unset dangerous vars
if [[ "$CONDA_PREFIX" != "" ]]; then
    echo "⚠️ Detected Conda environment. Cleaning environment variables..."
    unset LD_LIBRARY_PATH
fi

# Force good system libstdc++
SYSTEM_LIBSTDCPP=$(find /usr -name libstdc++.so.6 2>/dev/null | grep "/usr/lib/x86_64-linux-gnu/libstdc++.so.6" | head -n1)

if [[ -z "$SYSTEM_LIBSTDCPP" ]]; then
    echo "🛑 Could not find system libstdc++.so.6. Exiting."
    exit 1
fi

echo "✅ Using system libstdc++: $SYSTEM_LIBSTDCPP"
export LD_PRELOAD="$SYSTEM_LIBSTDCPP"

# Activate venv
source venv/bin/activate

# Print OpenGL Info
GL_VENDOR=$(glxinfo | grep "OpenGL vendor string" | cut -d':' -f2 | xargs || echo "Unknown")
GL_RENDERER=$(glxinfo | grep "OpenGL renderer string" | cut -d':' -f2 | xargs || echo "Unknown")
GL_VERSION_FULL=$(glxinfo | grep "OpenGL version string" | cut -d':' -f2 | xargs || echo "Unknown")

echo "🖥️ OpenGL Vendor : $GL_VENDOR"
echo "🖥️ OpenGL Renderer : $GL_RENDERER"
echo "🖥️ OpenGL Version : $GL_VERSION_FULL"

# Run the game
python3 src/main.py
