#!/usr/bin/env python3
"""
Reset MySQL Password Script
This script resets the MySQL root password to empty
"""

import subprocess
import os
import time

print("\n" + "="*70)
print("[MYSQL PASSWORD RESET]")
print("="*70)

# Create SQL file to reset password
reset_sql = """
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '';
"""

sql_file = "reset_password.sql"

try:
    # Write reset SQL to file
    with open(sql_file, 'w') as f:
        f.write(reset_sql)
    
    print("\n[1] Stopping MySQL service...")
    subprocess.run(['net', 'stop', 'MySQL80'], shell=True, capture_output=True)
    time.sleep(2)
    
    print("[2] Creating init file...")
    init_file = "init_password.txt"
    with open(init_file, 'w') as f:
        f.write("ALTER USER 'root'@'localhost' IDENTIFIED BY '';\nFLUSH PRIVILEGES;")
    
    print("[3] Starting MySQL with init file...")
    mysql_path = "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqld.exe"
    cmd = f'"{mysql_path}" --init-file="{os.path.abspath(init_file)}" --user=root'
    
    # Run in background
    import threading
    def run_mysql():
        subprocess.run(cmd, shell=True)
    
    thread = threading.Thread(target=run_mysql, daemon=True)
    thread.start()
    
    time.sleep(5)
    
    print("[4] Testing connection...")
    result = subprocess.run(
        ['mysql', '-u', 'root', '-e', 'SELECT 1'],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("\n[SUCCESS] MySQL root password reset to empty!")
        print("\nYou can now run: python FIX_DATABASE.py")
    else:
        print("\n[FAILED] Could not reset password")
        print("Try restarting MySQL service and retry")
    
    # Try to restart normal MySQL service
    time.sleep(2)
    print("\n[5] Restarting MySQL service...")
    subprocess.run(['net', 'start', 'MySQL80'], shell=True, capture_output=True)
    
    # Cleanup
    try:
        os.remove(sql_file)
        os.remove(init_file)
    except:
        pass

except Exception as e:
    print(f"\nError: {e}")

print("\n" + "="*70)
