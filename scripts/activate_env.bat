@echo off
REM Script to activate virtual environment
REM Usage: scripts\activate_env.bat

echo 🔄 Activating virtual environment...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set VENV_PATH=%PROJECT_ROOT%\venv

if exist "%VENV_PATH%" (
    call "%VENV_PATH%\Scripts\activate.bat"
    echo ✅ Virtual environment activated
    echo 📁 Project root: %PROJECT_ROOT%
    echo 🐍 Python: 
    where python
    echo.
    echo 🚀 You can now run:
    echo    python start_simple.py
    echo    python scripts\start.py
    echo    python scripts\test_platform.py
) else (
    echo ❌ Virtual environment not found at: %VENV_PATH%
    echo Please run setup first: scripts\setup.bat
) 