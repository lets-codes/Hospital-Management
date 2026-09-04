@echo off
REM ============================================================
REM Hospital Management System - Complete Startup Script
REM Run this as Administrator to start both MySQL and Flask
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Starting Hospital Management System
echo ============================================================
echo.

REM Ensure script is run as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo SOLUTION:
    echo 1. Right-click on this file (_START_SERVER_AND_MYSQL.bat)
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Determine script locations
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\"
set "LOGIN_DIR=%SCRIPT_DIR%"

REM Activate virtual environment if present
if exist "%ROOT_DIR%\.venv\Scripts\activate.bat" (
    call "%ROOT_DIR%\.venv\Scripts\activate.bat"
) else (
    echo [WARN] Virtual environment not found at "%ROOT_DIR%\.venv". Using system Python.
)

echo [1/4] Starting MySQL Service...
net start MySQL80 >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] MySQL80 service started
) else (
    echo [INFO] MySQL80 service already running or starting...
)

timeout /t 3 /nobreak

echo.
echo [2/4] Checking database setup...
cd /d "%LOGIN_DIR%"

REM Try to run database fix script
python FIX_DATABASE.py >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Database verified
) else (
    echo [INFO] Database setup returned an error. Please review FIX_DATABASE.py output.
)

timeout /t 2 /nobreak

echo.
echo [3/4] Starting Flask Server on http://localhost:5000...
echo.
echo ============================================================
echo Server is starting... Please wait
echo ============================================================
echo.

python server_patient_doctor.py

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Flask server exited with an error. Check the output above.
) else (
    echo.
    echo [OK] Flask server stopped.
)

echo.
pause
endlocal
