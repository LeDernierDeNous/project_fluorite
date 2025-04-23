@echo off
setlocal enabledelayedexpansion

echo 🎮 Starting the Game...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo 🛑 Python is not installed or not in PATH!
    echo Please install Python 3.x and try again.
    pause
    exit /b 1
)

:: Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo 🛑 Virtual environment not found! Run install.bat first.
    pause
    exit /b 1
)

:: Activate venv
call venv\Scripts\activate

:: Display system information
echo.
echo 🖥️ System Information:
echo Python Version: %PYTHON_VERSION%
echo Virtual Environment: %VIRTUAL_ENV%
echo.

:: Run the game
echo 🚀 Starting the game...
python src/main.py

:: If the game exits, keep the window open
if errorlevel 1 (
    echo.
    echo ❌ Game exited with an error.
    pause
) else (
    echo.
    echo ✅ Game exited successfully.
    pause
) 