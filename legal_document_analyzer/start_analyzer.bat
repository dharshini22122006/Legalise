@echo off
echo ========================================
echo    Legal Document Analyzer
echo    Powered by Granite AI Model
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting Legal Document Analyzer...
echo Application will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

python run.py

pause