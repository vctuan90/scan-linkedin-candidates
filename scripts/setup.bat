@echo off
echo 🚀 LinkedIn Profile Scraper API Setup (Windows)
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 📖 Please install Python 3.8 or higher from:
    echo    https://www.python.org/downloads/windows/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Setup ChromeDriver
echo 🌐 ChromeDriver will be downloaded automatically when needed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file with your LinkedIn credentials
) else (
    echo ✅ .env file already exists
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your LinkedIn credentials:
echo    notepad .env
echo.
echo 2. Start the API:
echo    python start.py
echo.
echo 3. Visit: http://localhost:8000/docs
echo.
echo For testing, run: python test_api.py
echo.
echo 📚 Windows notes:
echo    - Make sure Google Chrome browser is installed
echo    - If you encounter issues, run as Administrator
echo.
pause 