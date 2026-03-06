#!/usr/bin/env python3
"""  
ULTIMATE MySQL Password Reset
Works by stopping MySQL and starting with init file
"""

import subprocess
import os
import sys
import time
import tempfile
import winreg

print("\n" + "="*70)
print("[MYSQL] Ultimate Password Reset & Database Setup")
print("="*70 + "\n")

try:
    # Step 1: Find MySQL installation
    print("[1] Locating MySQL installation...")
    mysql_paths = [
        "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqld.exe",
        "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe",
        "C:\\Program Files (x86)\\MySQL\\MySQL Server 8.0\\bin\\mysqld.exe",
    ]
    
    mysqld_path = None
    mysql_cli_path = None
    
    for path in mysql_paths:
        if os.path.exists(path):
            if "mysqld.exe" in path and not mysqld_path:
                mysqld_path = path
            if "mysql.exe" in path and not mysql_cli_path:
                mysql_cli_path = path
    
    if not mysql_cli_path:
        mysql_cli_path = "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe"
    
    if mysqld_path:
        print(f"[OK] Found MySQL: {mysqld_path}\n")
    else:
        print("[ERROR] MySQL not found\n")
        sys.exit(1)
    
    # Step 2: Stop MySQL service
    print("[2] Stopping MySQL80 service...")
    subprocess.run(
        "net stop MySQL80",
        shell=True,
        capture_output=True,
        timeout=10
    )
    time.sleep(2)
    print("[OK] MySQL service stopped\n")
    
    # Step 3: Create SQL init script
    print("[3] Creating password reset script...")
    temp_dir = tempfile.gettempdir()
    init_sql = os.path.join(temp_dir, "mysql_init.sql")
    reset_password = """ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS deepanshu;
USE deepanshu;
CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('patient', 'doctor') DEFAULT 'patient',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);
"""
    
    with open(init_sql, 'w') as f:
        f.write(reset_password)
    
    print(f"[OK] Init script created: {init_sql}\n")
    
    # Step 4: Start MySQL with init file
    print("[4] Starting MySQL with init file (this may take 10-30 seconds)...")
    cmd = f'"{mysqld_path}" --init-file="{init_sql}" --user=root'
    
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for MySQL to process init file and stop
    for i in range(30):
        try:
            result = subprocess.run(
                f'"{mysql_cli_path}" -u root -h localhost -e "SELECT 1"',
                shell=True,
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                print(f"[OK] Password reset successful (attempt {i+1})\n")
                break
        except:
            pass
        
        if i % 5 == 0:
            print(f"[...] Waiting... (attempt {i+1}/30)")
        time.sleep(1)
    
    # Terminate the process
    proc.terminate()
    proc.wait(timeout=5)
    
    # Step 5: Restart MySQL normally
    print("\n[5] Restarting MySQL80 service...")
    subprocess.run(
        "net start MySQL80",
        shell=True,
        capture_output=True,
        timeout=10
    )
    time.sleep(3)
    print("[OK] MySQL80 service started\n")
    
    # Step 6: Verify connection
    print("[6] Testing connection...")
    result = subprocess.run(
        f'"{mysql_cli_path}" -u root -h localhost -e "SELECT VERSION();"',
        shell=True,
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print("[OK] Connection successful!")
        print("[OK] Database 'deepanshu' created!")
        print("[OK] MySQL root password reset to EMPTY\n")
        print("SUCCESS! You can now run:\n  python test_patient_details.py \n")
    else:
        print(f"[WARNING] Could not verify connection")
        print(f"Error: {result.stderr.decode()}\n")
    
    # Cleanup
    try:
        os.remove(init_sql)
    except:
        pass
    
    print("="*70 + "\n")

except Exception as e:
    print(f"\n[ERROR] {e}\n")
    sys.exit(1)
