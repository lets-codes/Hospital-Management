@echo off
setlocal EnableExtensions EnableDelayedExpansion

title Hospital Management System
color 0A

set "ROOT_DIR=%~dp0"
set "LOGIN_DIR=%ROOT_DIR%Login"
set "PYTHON_EXE=%ROOT_DIR%.venv\Scripts\python.exe"

if not exist "%LOGIN_DIR%\server_patient_doctor.py" (
    echo [ERROR] Could not find Login\server_patient_doctor.py
    pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python was not found. Install Python or create the project .venv.
        pause
        exit /b 1
    )
    set "PYTHON_EXE=python"
)

rem MySQL service control requires elevation. Re-run this same launcher as admin once.
net session >nul 2>&1
if errorlevel 1 (
    echo Requesting Administrator permission to start MySQL...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b 0
)

cls
echo ============================================================
echo        HOSPITAL MANAGEMENT SYSTEM - STARTING
echo ============================================================
echo.

echo [1/3] Starting MySQL...
netstat -ano | findstr /R /C:":3306 .*LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [OK] MySQL is already running.
) else (
    set "MYSQL_STARTED=0"
    for %%S in (MySQL80 MySQL57 MySQL MYSQLSERVER) do (
        if "!MYSQL_STARTED!"=="0" (
            net start "%%S" >nul 2>&1
            if not errorlevel 1 set "MYSQL_STARTED=1"
        )
    )
    timeout /t 3 /nobreak >nul
    netstat -ano | findstr /R /C:":3306 .*LISTENING" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] MySQL is not available on port 3306.
        echo Start MySQL manually, then run this file again.
        pause
        exit /b 1
    )
    echo [OK] MySQL is running.
)

echo [2/3] Starting Flask server...
start "Hospital Management Server" /D "%LOGIN_DIR%" "%PYTHON_EXE%" "server_patient_doctor.py"
if errorlevel 1 (
    echo [ERROR] Could not launch the Flask server.
    pause
    exit /b 1
)

echo [3/3] Opening the hospital system...
set "SERVER_READY=0"
for /l %%N in (1,1,15) do (
    netstat -ano | findstr /R /C:":5000 .*LISTENING" >nul 2>&1
    if not errorlevel 1 (
        set "SERVER_READY=1"
        goto :server_ready
    )
    timeout /t 1 /nobreak >nul
)

:server_ready
if "%SERVER_READY%"=="0" echo [WARN] Server is still starting; the browser may need a refresh.
start "" "http://localhost:5000/hospital_landing.html"

echo.
echo [OK] Hospital Management System is running.
echo     Web address: http://localhost:5000/hospital_landing.html
echo     Keep the server window open while using the system.
echo.
pause
endlocal