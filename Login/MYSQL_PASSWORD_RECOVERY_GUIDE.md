# MYSQL CONNECTION ERROR - FINAL SOLUTION GUIDE

## Problem
You're getting: "Could not connect to MySQL with default passwords"

**This means:** MySQL has a root password that was set during installation.

## ✅ FASTEST FIX (5 minutes)

### Option 1: Check Default MySQL Passwords
MySQL was likely installed with one of these passwords. Let me try them:

```powershell
# Run this in PowerShell as Administrator:

# Try password: "root"
mysql -u root -proot -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';FLUSH PRIVILEGES;"

# OR try: "password" 
mysql -u root -ppassword -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';FLUSH PRIVILEGES;"

# OR try: "mysql"
mysql -u root -pmysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';FLUSH PRIVILEGES;"
```

If one of these works, you'll see: `Empty set` (no error)

Then continue to next step.

---

### Option 2: You Set a Custom Password

If you remember the password you set during MySQL installation:

```powershell
# Use YOUR_PASSWORD here:
mysql -u root -pYOUR_PASSWORD -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';FLUSH PRIVILEGES;"
```

---

### Option 3: Generate Temporary Password from MySQL Logs

Check Windows Event Viewer for the temporary password MySQL generated:

1. Press `Win + R`
2. Type: `eventvwr.msc`
3. Go to: Windows Logs → Application
4. Look for "MySQL" entries
5. You may find a temporary password like: `xxxxxxxxxxxxxx`

Use that temporary password:
```powershell
mysql -u root -pTEMPORARY_PASSWORD -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '';FLUSH PRIVILEGES;"
```

---

## After Resetting Password

Once any of the above commands work, run:

```powershell
cd "d:\Storage Box\Computer Input\Visual Studio\Project\Shivani Anand\Hospital Management\Login"
python FIX_DATABASE.py
```

Then:
```powershell
python server_patient_doctor.py
```

---

## 🔧 MANUAL FALLBACK: Edit Code with Known Password

If you know the MySQL root password, just edit this file:

**File:** `server_patient_doctor.py`  
**Line:** 22 (find `'password': ''`)  
**Change to:** `'password': 'YOUR_KNOWN_PASSWORD'`

Then save and run:
```powershell
python server_patient_doctor.py
python FIX_DATABASE.py
python test_patient_details.py
```

---

## 🆘 LAST RESORT: Full MySQL Reinstall

If nothing works:

1. Go to: Control Panel → Add/Remove Programs
2. Find and uninstall MySQL 8.0
3. Delete folder: `C:\Program Files\MySQL`
4. Delete folder: `C:\ProgramData\MySQL`
5. Restart your computer
6. Download fresh MySQL from: https://dev.mysql.com/downloads/mysql/
7. Install with NO password (leave password field empty)
8. Run: `python FIX_DATABASE.py`

---

## ✓ Quick Test Commands

After resetting password, test with:

```powershell
# Should show no errors:
mysql -u root -e "SELECT 1"

# Should show 'deepanshu' database:
mysql -u root -e "SHOW DATABASES"
```

---

**Need help?** Try the commands above in order. One should work!
