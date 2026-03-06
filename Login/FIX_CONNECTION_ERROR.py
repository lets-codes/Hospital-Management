#!/usr/bin/env python3
"""
Fix Connection Error - Complete Diagnostic and Setup Tool
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
            if result.stderr:
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
    print("\n[1] Checking MySQL Service Status...")
    print("-" * 70)
    
    success, output, _ = run_cmd('netstat -ano | findstr ":3306"', show_output=False)
    
    if success and output:
        print("[✓] MySQL is RUNNING on port 3306")
        return True
    else:
        print("[✗] MySQL is NOT running")
        print("\nAttempting to start MySQL80 service...")
        print("(If you see 'Access Denied', run this script as Administrator)")
        
        success, _, _ = run_cmd('net start MySQL80', show_output=False)
        time.sleep(3)
        
        if success:
            print("[✓] MySQL started successfully")
            time.sleep(2)
            return True
        else:
            print("[!] Could not start MySQL80 - trying alternative methods...")
            # Try other service names
            alt_services = ['MySQL57', 'MySQL', 'MYSQL']
            for service in alt_services:
                success, _, _ = run_cmd(f'net start {service}', show_output=False)
                if success:
                    print(f"[✓] Started {service} service")
                    time.sleep(2)
                    return True
            
            print("[!] Could not start any MySQL service")
            print("\nDo this manually:")
            print("  1. Open Services (services.msc)")
            print("  2. Find 'MySQL80' or similar")
            print("  3. Right-click and select 'Start'")
            return False

def test_db_connection():
    """Test database connection"""
    print("\n[2] Testing Database Connection...")
    print("-" * 70)
    
    # Try different credentials
    credentials = [
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'user': 'root', 'password': 'password'},
        {'host': 'localhost', 'user': 'root', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': 'root'},
    ]
    
    for cred in credentials:
        try:
            conn = mysql.connector.connect(**cred)
            print(f"[✓] Connected with: user={cred['user']}, password={cred['password']}")
            return conn
        except Error as e:
            error_code = str(e).split('Error')[0].strip() if 'Error' in str(e) else str(e)
            print(f"[✗] Failed with: {cred['user']}/{cred['password']} - {error_code}")
            continue
    
    print("\n[!] Could not connect to MySQL with any credential")
    return None

def setup_database(conn):
    """Create database and tables"""
    print("\n[3] Setting Up Database Schema...")
    print("-" * 70)
    
    try:
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS deepanshu")
        print("[✓] Database 'deepanshu' ready")
        
        # Switch to database
        cursor.execute("USE deepanshu")
        
        # Create login table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[✓] Table 'login' ready")
        
        # Create doctor table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                specialization VARCHAR(255),
                license_number VARCHAR(255),
                experience_years INT,
                consultation_fee DECIMAL(10, 2),
                FOREIGN KEY (user_id) REFERENCES login(id)
            )
        """)
        print("[✓] Table 'doctors' ready")
        
        # Create patient table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                age INT,
                medical_history TEXT,
                FOREIGN KEY (user_id) REFERENCES login(id)
            )
        """)
        print("[✓] Table 'patients' ready")
        
        conn.commit()
        print("\n[✓] Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"[!] Database error: {e}")
        return False

def check_port_5000():
    """Check if Flask port is available"""
    print("\n[4] Checking Port 5000 (Flask)...")
    print("-" * 70)
    
    success, output, _ = run_cmd('netstat -ano | findstr ":5000"', show_output=False)
    
    if success and output:
        print("[!] Port 5000 is in use!")
        print("Kill process or use different port")
        return False
    else:
        print("[✓] Port 5000 is available")
        return True

def main():
    print("\n" + "="*70)
    print("  HOSPITAL MANAGEMENT - CONNECTION ERROR FIX")
    print("="*70)
    
    print("\nThis tool will:")
    print("  1. Check if MySQL is running")
    print("  2. Test database connection")
    print("  3. Create necessary tables")
    print("  4. Verify Flask port")
    
    # Step 1: Check MySQL
    if not check_mysql_running():
        print("\n[WARNING] MySQL may not be running properly")
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            print("Exiting...")
            return
    
    time.sleep(2)
    
    # Step 2: Test connection
    conn = test_db_connection()
    if not conn:
        print("\n[CRITICAL] Cannot connect to MySQL")
        print("\nSolutions:")
        print("  1. Ensure MySQL is running (check Services)")
        print("  2. Verify MySQL user 'root' exists")
        print("  3. Try resetting MySQL password")
        return
    
    # Step 3: Setup database
    if not setup_database(conn):
        print("\n[ERROR] Could not setup database")
        conn.close()
        return
    
    conn.close()
    
    # Step 4: Check port
    check_port_5000()
    
    print("\n" + "="*70)
    print("  SETUP COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Start the server: python server_patient_doctor.py")
    print("  2. Server will run on http://localhost:5000")
    print("  3. Open http://localhost:5000 in your browser")

if __name__ == '__main__':
    main()
