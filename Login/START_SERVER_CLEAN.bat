@echo off
REM Clean Flask Server Startup - No Emojis, No Frills
cd /d "d:\Storage Box\Computer Input\Visual Studio\Project\Shivani Anand\Hospital Management\Login"

REM Kill any existing Flask processes
taskkill /F /IM python.exe 2>nul

REM Wait a moment
timeout /t 2 /nobreak

REM Start server with UTF-8 encoding
echo Starting Flask server...
echo.
set PYTHONIOENCODING=utf-8
python server_patient_doctor.py
