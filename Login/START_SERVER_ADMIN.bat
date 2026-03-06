@echo off
REM ===================================================================
REM  HOSPITAL MANAGEMENT SYSTEM - STARTUP SCRIPT
REM  Run this as Administrator to fix connection errors
REM ===================================================================

echo.
echo ===================================================================
echo   HOSPITAL MANAGEMENT - COMPLETE STARTUP
echo ===================================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] This script must run as Administrator!
    echo.
    echo Steps to fix:
    echo 1. Right-click this batch file
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b
)

echo [1/3] Checking MySQL Service...
echo.

REM Check if MySQL is running
netstat -ano | findstr ":3306" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] MySQL is already running
) else (
    echo [!] MySQL is not running - Starting...
    net start MySQL80
    if %ERRORLEVEL% NEQ 0 (
        echo [!] Could not start MySQL80, trying alternatives...
        net start MySQL57
    )
    timeout /t 5 /nobreak
)

echo.
echo [2/3] Checking Port 5000...
echo.

netstat -ano | findstr ":5000" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [!] Port 5000 is already in use - killing process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do taskkill /pid %%a /f >nul 2>&1
    timeout /t 2 /nobreak
) else (
    echo [OK] Port 5000 is free
)

echo.
echo [3/3] Starting Flask Server...
echo.
echo ===================================================================
echo   The server will start below. Visit http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ===================================================================
echo.

REM Start the Flask server
python server_patient_doctor.py

pause
