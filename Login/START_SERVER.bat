@echo off
REM Hospital Management System - Quick Start Server
REM This batch file starts MySQL and the Flask server automatically

setlocal enabledelayedexpansion

cls
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║        🏥 HOSPITAL MANAGEMENT SYSTEM - AUTO START                     ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ and add it to your PATH
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [Step 1/3] Checking for MySQL service...
echo.

REM Check if MySQL is running
tasklist | find /I "MySQLServer.EXE" >nul
if errorlevel 1 (
    echo [*] MySQL not running, attempting to start...
    
    REM Try to start MySQL80
    net start MySQL80 >nul 2>&1
    if errorlevel 1 (
        REM Try MySQL57
        net start MySQL57 >nul 2>&1
        if errorlevel 1 (
            REM Try generic MySQL
            net start MySQL >nul 2>&1
            if errorlevel 1 (
                echo.
                echo ⚠️  Could not auto-start MySQL
                echo.
                echo Please start MySQL manually:
                echo  1. Press Windows Key + R
                echo  2. Type: services.msc
                echo  3. Find MySQL service and click "Start"
                echo  4. Then run this batch file again
                echo.
                pause
                exit /b 1
            )
        )
    )
    
    echo [✓] MySQL started successfully
    timeout /t 3 /nobreak
) else (
    echo [✓] MySQL is already running
)

echo.
echo [Step 2/3] Clearing port 5000...
echo.

REM Kill any process on port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000"') do (
    echo [*] Killing process on port 5000...
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 1 /nobreak

echo [✓] Port 5000 is ready
echo.
echo [Step 3/3] Starting Flask Server...
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Start the Flask server
python START_SERVER_FIXED.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to start server
    echo.
    echo Run this for more details:
    echo   python FIX_CONNECTION_ERROR.py
    echo.
    pause
    exit /b 1
)

pause
