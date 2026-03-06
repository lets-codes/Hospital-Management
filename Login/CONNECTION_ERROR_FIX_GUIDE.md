# Connection Error Fix Guide

## ❌ Problem: "Connection error. Make sure the server is running on localhost:5000"

This error occurs when your Python test scripts cannot connect to the Flask server. Here's how to fix it.

---

## 🔧 Quick Fix (Recommended)

### Option 1: Use the Python Server Startup Script (EASIEST)
1. **Right-click** on `START_SERVER.py`
2. Open Command Prompt or PowerShell **as Administrator**
3. Run this command:
```powershell
python START_SERVER.py
```

This script will:
- ✓ Start MySQL database service
- ✓ Setup the database automatically
- ✓ Start the Flask server on localhost:5000

---

### Option 2: Use the Batch File
1. **Right-click** on `_START_SERVER_AND_MYSQL.bat`
2. Select **"Run as administrator"**
3. The server will start automatically

---

## 🔍 Root Causes & Solutions

### Root Cause 1: MySQL Service Not Running

**Symptoms:**
- Server starts but times out on requests
- Database connection errors in server logs

**Solution:**
```powershell
# Run as Administrator in PowerShell
net start MySQL80
```

---

### Root Cause 2: MySQL Data Directory Missing

**Symptoms:**
- MySQL fails to start with permission errors
- "Can't create test file" errors

**Solution:**
Run the Python startup script which handles this automatically:
```powershell
python START_SERVER.py
```

---

### Root Cause 3: Port 5000 Already in Use

**Symptoms:**
- "Address already in use" error when starting server

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PROCESSID)
taskkill /PID PROCESSID /F
```

---

## ✅ Verification Steps

### Step 1: Verify MySQL is Running
```powershell
netstat -ano | findstr :3306
```
You should see: `TCP    127.0.0.1:3306         0.0.0.0:0              LISTENING`

### Step 2: Verify Flask Server is Running
```powershell
netstat -ano | findstr :5000
```
You should see: `TCP    127.0.0.1:5000         0.0.0.0:0              LISTENING`

### Step 3: Test Health Endpoint
```powershell
python -c "import requests; r = requests.get('http://localhost:5000/health'); print(r.status_code, r.text)"
```
You should see: `200 {"status":"ok",...}`

---

## 🚀 Complete Startup Sequence

If you want to do it manually:

### 1. Start MySQL Service
```powershell
# Run as Administrator
net start MySQL80
```

### 2. Wait for MySQL (about 3-5 seconds)

### 3. Setup Database
```powershell
python FIX_DATABASE.py
```

### 4. Start Flask Server
```powershell
cd "d:\Storage Box\Computer Input\Visual Studio\Project\Shivani Anand\Hospital Management\Login"
python server_patient_doctor.py
```

### 5. In another terminal, run your tests
```powershell
python test_patient_details.py
```

---

## 🛠️ Troubleshooting Advanced Issues

### Access Denied When Starting MySQL
**Cause:** Not running as Administrator

**Fix:**
1. Right-click on PowerShell
2. Select "Run as administrator"
3. Run the startup script or commands

### MySQL Service Doesn't Exist
**Cause:** MySQL not properly installed

**Fix:**
1. Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
2. Install and check "Configure MySQL Server now"
3. Follow installation wizard

### Python Can't Import Modules
**Cause:** Required packages not installed

**Fix:**
```powershell
pip install flask flask-cors mysql-connector-python bcrypt requests
```

### Database Already Exists Error
**Cause:** Database partially set up

**Fix:**
```powershell
python FIX_DATABASE.py
```
This script handles existing databases properly.

---

## 📋 Checklist for Success

After completing the fix, verify:

- [ ] MySQL80 service is running (`net start MySQL80` shows no errors)
- [ ] Port 3306 is listening (`netstat -ano | findstr :3306`)
- [ ] Port 5000 is listening (`netstat -ano | findstr :5000`)
- [ ] Health endpoint responds (`curl http://localhost:5000/health`)
- [ ] Flask server shows startup message
- [ ] Test runs without connection errors

---

## 🆘 Still Not Working?

If you've tried all the above:

1. **Check MySQL logs:**
   - Windows Event Viewer → Applications → Look for MySQL errors

2. **Verify Python environment:**
```powershell
python --version
pip list | findstr -i "flask|mysql|requests"
```

3. **Test MySQL directly:**
```powershell
mysql -u root -h localhost
```

4. **Kill all Python processes and restart:**
```powershell
taskkill /F /IM python.exe
```

5. **Restart your computer** - This often fixes permission and service issues

---

## 📞 Emergency Fallback

If nothing else works, run this minimal test:

```powershell
# This shows the exact error
python test_patient_details.py
```

Copy the exact error message and check it against the solutions above.

---

## 🎯 Next Steps

Once the connection is fixed:

1. Run your test file: `python test_patient_details.py`
2. Access the web interface: http://localhost:5000/hospital_landing.html
3. Test all features as needed

**Server will run indefinitely until you press Ctrl+C to stop it.**

---

Last Updated: February 17, 2026
