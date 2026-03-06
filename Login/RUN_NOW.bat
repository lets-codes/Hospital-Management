@echo off
REM === QUICK START MYSQL + SERVER ===
REM This script automatically starts both MySQL and the Flask server

echo.
echo Starting Hospital Management System...
echo.

REM Step 1: Check if running as admin
net session >nul 2>&1
if errorlevel 1 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~f0' -Verb RunAs"
    exit /b
)

echo [√] Running as Administrator
echo.
echo [1/2] Starting MySQL Service...

REM Try to start MySQL80
net start MySQL80 >nul 2>&1
if errorlevel 0 (
    echo [√] MySQL started
) else (
    echo [!] MySQL might already be running
)

echo [√] Waiting 3 seconds for MySQL to initialize...
timeout /t 3 /nobreak

echo.
echo [2/2] Starting Flask Server...
echo.
echo ════════════════════════════════════════════════════════════
echo   Hospital Management System is starting...
echo.
echo   Once you see:
echo   "Running on http://127.0.0.1:5000"
echo.
echo   Open your browser to: http://localhost:5000
echo ════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"
python server_patient_doctor.py

echo.
echo Server stopped. Press any key to close...
pause >nul
