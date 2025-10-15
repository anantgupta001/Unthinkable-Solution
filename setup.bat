@echo off
REM Knowledge Base Search Engine - Setup Script (Windows)
REM This script automates the installation process

echo 🔍 Knowledge Base Search Engine - Setup
echo ========================================
echo.

REM Check Python version
echo 📋 Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv
echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo ✅ pip upgraded
echo.

REM Install dependencies
echo 📦 Installing dependencies (this may take a few minutes)...
cd backend
pip install -r requirements.txt
cd ..
echo ✅ All dependencies installed
echo.

REM Create docs directory if it doesn't exist
echo 📁 Setting up documents folder...
if not exist "backend\app\docs" mkdir backend\app\docs
echo ✅ Documents folder ready
echo.

REM Success message
echo 🎉 Setup complete!
echo.
echo 📖 Next steps:
echo 1. Add your documents (.txt or .pdf) to: backend\app\docs\
echo 2. Start the backend: cd backend ^&^& uvicorn app.main:app --reload
echo 3. Open frontend\index.html in your browser
echo.
echo For detailed instructions, see README.md
echo.
pause

