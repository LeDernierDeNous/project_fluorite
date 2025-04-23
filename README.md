# Ultra-Pro Game

Welcome to Ultra-Pro! This README will guide you through the installation and launch process of the game.

## Prerequisites

Before installing the game, make sure you have the following installed:

- Python 3.x
- pip (Python package installer)
- OpenGL 3.0 or higher (for Linux users)

## Installation

### Windows Installation

1. Open Command Prompt or PowerShell in the game directory
2. Run the installation script:
   ```
   install.bat
   ```
   This will:
   - Check for Python installation
   - Create a virtual environment
   - Install required dependencies

### Linux Installation

1. Open Terminal in the game directory
2. Make the installation script executable:
   ```
   chmod +x install.sh
   ```
3. Run the installation script:
   ```
   ./install.sh
   ```
   This will:
   - Check for required system packages
   - Verify OpenGL version
   - Create a virtual environment
   - Install required dependencies

## Launching the Game

### Windows

1. Simply run:
   ```
   start.bat
   ```
   This will:
   - Activate the virtual environment
   - Display system information
   - Launch the game

### Linux

1. Make the start script executable:
   ```
   chmod +x start.sh
   ```
2. Run the game:
   ```
   ./start.sh
   ```
   This will:
   - Activate the virtual environment
   - Display OpenGL information
   - Launch the game

## Troubleshooting

### Common Issues

- **Python not found**: Make sure Python is installed and added to your system's PATH
- **Virtual environment issues**: Try deleting the `venv` folder and running the installation script again
- **OpenGL issues (Linux)**: Ensure your graphics drivers are up to date and OpenGL 3.0 or higher is supported

### Windows Specific

- If you see "Python is not installed" error, download and install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### Linux Specific

- If you see missing package errors, run:
  ```
  sudo apt update
  sudo apt install python3 python3-venv python3-pip mesa-utils
  ```
- For OpenGL issues, update your graphics drivers and Mesa libraries

## Support

If you encounter any issues not covered in this README, please check the game's documentation or contact support.
