@echo off
REM ============================================================
REM Hospital Management System - Complete Startup Script
REM Run this as Administrator to start both MySQL and Flask
REM ============================================================

echo.
echo ============================================================
echo Starting Hospital Management System
echo ============================================================
echo.

REM Check if running as administrator
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

echo [1/3] Starting MySQL Service...
net start MySQL80 >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] MySQL80 service started
) else (
    echo [INFO] MySQL80 service already running or starting...
)

timeout /t 3 /nobreak

echo.
echo [2/3] Checking database setup...
cd /d "d:\Storage Box\Computer Input\Visual Studio\Project\Shivani Anand\Hospital Management\Login"

REM Try to run database fix script
python FIX_DATABASE.py >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Database verified
) else (
    echo [INFO] Database setup in progress...
)

timeout /t 2 /nobreak

echo.
echo [3/3] Starting Flask Server on http://localhost:5000...
echo.
echo ============================================================
echo Server is starting... Please wait
echo ============================================================
echo.

python server_patient_doctor.py

echo.
echo Server stopped.
pause
