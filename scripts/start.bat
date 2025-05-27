@echo off
echo 🚀 Starting LinkedIn Profile Scraper API (Windows)
echo ===================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Start the API
echo 🚀 Starting API server...
python start.py

pause 