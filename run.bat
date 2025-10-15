@echo off
REM Quick start script for Knowledge Base Search Engine (Windows)

echo 🚀 Starting Knowledge Base Search Engine...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Start backend
echo 🔧 Starting backend server...
echo 📍 API will be available at: http://127.0.0.1:8000
echo 📖 API docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
uvicorn app.main:app --reload

