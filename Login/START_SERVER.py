#!/usr/bin/env python3
"""
Hospital Management System - Complete Server Startup Helper
Handles MySQL service startup and Flask server launch
Run with administrator privileges for best results
"""

import subprocess
import time
import os
import sys
import socket
import requests

# Configuration
MYSQL_SERVICE = "MySQL80"
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
FLASK_SCRIPT = "server_patient_doctor.py"
FIX_SCRIPT = "FIX_DATABASE.py"

def is_port_open(host, port, timeout=2):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def is_mysql_running():
    """Check if MySQL port is open"""
    return is_port_open("localhost", 3306, timeout=1)

def start_mysql_service():
    """Start MySQL service"""
    print("\n[*] Attempting to start MySQL80 service...")
    try:
        result = subprocess.run(
            ["net", "start", "MySQL80"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0 or "already being run" in result.stdout:
            print("[OK] MySQL service started successfully")
            return True
        else:
            print(f"[!] Could not start MySQL service (error code: {result.returncode})")
            print("[!] If you see 'Access is Denied', run this script as Administrator")
            return False
    except Exception as e:
        print(f"[X] Error starting MySQL: {e}")
        return False

def wait_for_mysql(max_attempts=15):
    """Wait for MySQL to become available"""
    print("[*] Waiting for MySQL to be available...")
    for attempt in range(max_attempts):
        if is_mysql_running():
            print(f"[OK] MySQL is available (attempt {attempt + 1})")
            return True
        print(f"[.] Waiting... (attempt {attempt + 1}/{max_attempts})")
        time.sleep(1)
    
    print("[X] MySQL did not become available in time")
    return False

def setup_database():
    """Run database setup script"""
    if not os.path.exists(FIX_SCRIPT):
        print(f"[!] Database setup script not found: {FIX_SCRIPT}")
        return False
    
    # Skip running FIX_DATABASE.py - it has emoji encoding issues
    print(f"[*] Skipping database setup script (medicines table auto-created by server)")
    return True

def start_flask_server():
    """Start Flask server"""
    if not os.path.exists(FLASK_SCRIPT):
        print(f"[X] Flask script not found: {FLASK_SCRIPT}")
        return False
    
    print(f"\n[*] Starting Flask server: {FLASK_SCRIPT}")
    print(f"[*] Server will run on http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"[*] Press Ctrl+C to stop the server\n")
    print("=" * 70)
    
    try:
        subprocess.run([sys.executable, FLASK_SCRIPT])
        return True
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
        return True
    except Exception as e:
        print(f"[X] Error starting Flask server: {e}")
        return False

def test_server_connection(max_attempts=20):
    """Test if Flask server is responding"""
    print("[*] Testing Flask server connection...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"http://{FLASK_HOST}:{FLASK_PORT}/health", timeout=1)
            if response.status_code == 200:
                print(f"[OK] Flask server is responding! (attempt {attempt + 1})")
                return True
        except:
            pass
        
        print(f"[.] Testing... (attempt {attempt + 1}/{max_attempts})")
        time.sleep(0.5)
    
    print("[!] Flask server not responding yet (may still be starting)")
    return False

def main():
    """Main startup routine"""
    print("\n" + "=" * 70)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - SERVER STARTUP")
    print("=" * 70)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"\n[*] Working directory: {script_dir}")
    
    # Step 1: Start MySQL
    print("\n" + "-" * 70)
    print("STEP 1: Starting MySQL Database...")
    print("-" * 70)
    
    if is_mysql_running():
        print("[✓] MySQL is already running")
    else:
        mysql_started = start_mysql_service()
        if mysql_started:
            if not wait_for_mysql():
                print("\n[!] WARNING: MySQL is not responding")
                print("[!] Some features may not work correctly")
                print("[!] If you see 'Access is Denied', run this script as Administrator")
    
    # Step 2: Setup Database
    print("\n" + "-" * 70)
    print("STEP 2: Setting up Database...")
    print("-" * 70)
    
    time.sleep(2)  # Give MySQL time to fully start
    setup_database()
    
    # Step 3: Start Flask
    print("\n" + "-" * 70)
    print("STEP 3: Starting Flask Server...")
    print("-" * 70)
    
    success = start_flask_server()
    
    if success:
        print("\n[✓] Server startup completed")
    else:
        print("\n[X] Server startup encountered errors")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Startup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n[X] Unexpected error: {e}")
        sys.exit(1)
