@echo off
setlocal enabledelayedexpansion

echo 🔵 Starting Ultra-Pro Setup...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo 🛑 Python is not installed or not in PATH!
    echo Please install Python 3.x from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo 🛑 pip is not installed!
    echo Please install pip and try again.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate venv
call venv\Scripts\activate

:: Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo 📚 Installing Python libraries...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo ⚠️ requirements.txt not found!
)

echo.
echo ✅ Ultra-Pro Installation Finished!
echo 👉 You can now start the game with start.bat
pause 