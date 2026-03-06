#!/usr/bin/env python3
"""
Complete Server Startup Script - Fixes Connection Issues
This script ensures MySQL is running and starts the Flask server properly
"""

import subprocess
import sys
import os
import time
import mysql.connector
from mysql.connector import Error

def run_cmd(command, show_output=True):
    """Execute a command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if show_output:
            print(result.stdout)
            if result.stderr and 'warning' not in result.stderr.lower():
                print(result.stderr)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"[!] Timeout running: {command}")
        return False, "", "Timeout"
    except Exception as e:
        print(f"[!] Error: {e}")
        return False, "", str(e)

def check_mysql_running():
    """Check if MySQL port 3306 is listening"""
    print("\n" + "="*70)
    print("[STEP 1] Checking MySQL Database Service...")
    print("="*70)
    
    success, output, _ = run_cmd('netstat -ano | findstr ":3306"', show_output=False)
    
    if success and output:
        print("[✓] MySQL is RUNNING on port 3306")
        return True
    else:
        print("[✗] MySQL is NOT running - Attempting to start...\n")
        
        # Try to start MySQL80
        print("Starting MySQL80 service...")
        success, _, _ = run_cmd('net start MySQL80', show_output=False)
        
        if success:
            print("[✓] MySQL80 started successfully")
            time.sleep(3)
            return True
        
        # Try alternative service names
        alt_services = ['MySQL57', 'MYSQL', 'MySQL']
        for service in alt_services:
            print(f"Trying {service}...")
            success, _, _ = run_cmd(f'net start {service}', show_output=False)
            if success:
                print(f"[✓] {service} started successfully")
                time.sleep(3)
                return True
        
        print("\n[!] Could not auto-start MySQL")
        print("\n⚠️  MANUAL FIX REQUIRED:")
        print("  1. Open Services (Windows + R, type 'services.msc', press Enter)")
        print("  2. Find 'MySQL' service (MySQL80, MySQL57, etc.)")
        print("  3. Right-click and select 'Start'")
        print("  4. Then run this script again\n")
        return False

def test_db_connection():
    """Test database connection with multiple credential attempts"""
    print("\n" + "="*70)
    print("[STEP 2] Testing Database Credentials...")
    print("="*70)
    
    credentials = [
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'user': 'root', 'password': 'password'},
        {'host': 'localhost', 'user': 'root', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': 'root'},
    ]
    
    for i, cred in enumerate(credentials, 1):
        try:
            conn = mysql.connector.connect(**cred)
            pwd_display = cred['password'] if cred['password'] else '(empty)'
            print(f"[✓] Connected successfully: user='{cred['user']}', password='{pwd_display}'")
            return conn, cred
        except Error as e:
            pwd_display = cred['password'] if cred['password'] else '(empty)'
            print(f"[✗] Attempt {i} failed: {cred['user']}/{pwd_display}")
            continue
    
    print("\n[!] Could not connect with any credential")
    print("    Check if MySQL is actually running (Step 1)")
    return None, None

def ensure_database_exists(conn, cred):
    """Ensure the deepanshu database exists"""
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS deepanshu")
        cursor.execute("USE deepanshu")
        print("[✓] Database 'deepanshu' is ready")
        cursor.close()
        return True
    except Error as e:
        print(f"[!] Error creating database: {e}")
        return False

def stop_existing_flask_server():
    """Kill any Flask server already running on port 5000"""
    print("\n" + "="*70)
    print("[STEP 3] Clearing Port 5000...")
    print("="*70)
    
    # Try to find and kill process on port 5000
    success, output, _ = run_cmd('netstat -ano | findstr ":5000"', show_output=False)
    
    if success and output:
        print("[*] Found process on port 5000, cleaning up...")
        try:
            lines = output.strip().split('\n')
            if lines and len(lines) > 0:
                parts = lines[0].split()
                if parts:
                    pid = parts[-1]
                    run_cmd(f'taskkill /PID {pid} /F', show_output=False)
                    print("[✓] Cleaned up port 5000")
                    time.sleep(1)
        except:
            pass
    else:
        print("[✓] Port 5000 is available")

def start_flask_server():
    """Start the Flask server"""
    print("\n" + "="*70)
    print("[STEP 4] Starting Flask Server...")
    print("="*70)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_file = os.path.join(script_dir, 'server_patient_doctor.py')
    
    if not os.path.exists(server_file):
        print(f"[!] Server file not found: {server_file}")
        return False
    
    print(f"[*] Starting server from: {server_file}")
    print("\n" + "="*70)
    
    try:
        # Start the Flask server in a new window so it stays running
        subprocess.Popen(
            f'start cmd /k "cd /d {script_dir} && python server_patient_doctor.py"',
            shell=True
        )
        
        print("[✓] Flask server started!")
        print("\n" + "="*70)
        print("✅ SERVER READY")
        print("="*70)
        print("\nYour hospital system is now accessible at:")
        print("  🌐 http://localhost:5000/hospital_landing.html")
        print("\nOr open any HTML file:")
        print("  📄 login.html")
        print("  📄 signup.html")
        print("  📄 hospital_landing.html")
        print("\nThe server will continue running in a separate window.")
        print("Do NOT close that window or the server will stop.\n")
        
        return True
    except Exception as e:
        print(f"[!] Error starting server: {e}")
        return False

def main():
    """Main execution"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🏥 HOSPITAL MANAGEMENT SYSTEM - SERVER STARTUP".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Step 1: Check MySQL
    if not check_mysql_running():
        print("\n⚠️  Please start MySQL manually and run this script again.")
        input("\nPress Enter to exit...")
        return
    
    # Step 2: Test database connection
    conn, cred = test_db_connection()
    if not conn:
        print("\n⚠️  Could not connect to database. Check MySQL is running.")
        input("\nPress Enter to exit...")
        return
    
    # Step 3: Ensure database exists
    if not ensure_database_exists(conn, cred):
        print("\n[!] Warning: Database setup had issues, but trying to start server anyway...")
    
    if conn:
        conn.close()
    
    # Step 4: Clear port 5000
    stop_existing_flask_server()
    
    # Step 5: Start Flask server
    time.sleep(1)
    if start_flask_server():
        print("✅ All systems ready! The server will run in a new window.")
        time.sleep(3)
    else:
        print("\n[!] Failed to start Flask server")
        input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
