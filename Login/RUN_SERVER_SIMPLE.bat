@echo off
REM Hospital Management System - SIMPLE START
REM This file starts the server - that's it!

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  🏥 Hospital Management System - Starting Server              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Starting server on http://localhost:5000/
echo.
echo ⚠️  IMPORTANT:
echo    - Do NOT close this window!
echo    - Keep this window open while using the system
echo    - If you close it, the system will stop working
echo.
echo Starting in 2 seconds...
echo.

timeout /t 2

python server_patient_doctor.py

pause
