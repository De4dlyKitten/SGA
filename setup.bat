@echo off
echo =========================================
echo    SGA-Lite - Quick Start Setup
echo =========================================
echo.

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Python not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

python --version

REM Create virtual environment
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
) else (
    echo [+] Virtual environment already exists
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt --quiet

REM Setup .env
if not exist ".env" (
    echo [*] Creating .env file...
    copy .env.example .env
) else (
    echo [+] .env file already exists
)

REM Run migrations
echo [*] Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Seed database
echo [*] Seeding database with initial data...
python manage.py seed_data

echo.
echo =========================================
echo    Setup Complete!
echo =========================================
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
echo Then visit: http://localhost:8000
echo.
echo Default credentials:
echo   Admin:    admin / admin123
echo   Employee: employee1 / password123
echo.
pause
