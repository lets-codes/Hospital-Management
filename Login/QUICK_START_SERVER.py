#!/usr/bin/env python3
"""
One-Click Server Starter
This script handles everything needed to fix the connection error
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description, show_output=True):
    """Run a command and report results"""
    print(f"\n[•] {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        if show_output and result.stdout:
            print(result.stdout)
        if result.returncode != 0 and show_output and result.stderr:
            print(f"[!] Error: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[!] Command timed out")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print(" HOSPITAL MANAGEMENT SYSTEM - Connection Error Fix")
    print("="*70 + "\n")
    
    print("This script will fix the 'Connection error on localhost:5000' issue.\n")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"Project Directory: {script_dir}\n")
    
    # Step 1: Check if MySQL is running
    print("[1/5] Checking MySQL Service...")
    print("-" * 70)
    
    mysql_running = run_command(
        'netstat -ano | findstr ":3306"',
        "Checking MySQL port",
        show_output=False
    )
    
    if mysql_running:
        print("[✓] MySQL is already running")
    else:
        print("[!] MySQL is not running")
        print("[•] Attempting to start MySQL80 service...")
        print("    NOTE: If you see 'Access is Denied':")
        print("    • Right-click Command Prompt/PowerShell")
        print("    • Select 'Run as administrator'")
        print("    • Then run this script again\n")
        
        run_command(
            'net start MySQL80',
            "Starting MySQL service",
            show_output=False
        )
        time.sleep(3)
    
    # Step 2: Setup database
    print("\n[2/5] Setting up Database...")
    print("-" * 70)
    
    if os.path.exists("FIX_DATABASE.py"):
        run_command(
            f'{sys.executable} FIX_DATABASE.py',
            "Running database setup",
            show_output=True
        )
    else:
        print("[!] FIX_DATABASE.py not found - skipping")
    
    # Step 3: Check port availability
    print("\n[3/5] Checking Port Availability...")
    print("-" * 70)
    
    port_available = not run_command(
        'netstat -ano | findstr ":5000"',
        "Checking if port 5000 is free",
        show_output=False
    )
    
    if port_available:
        print("[✓] Port 5000 is available")
    else:
        print("[!] Port 5000 is already in use - will try anyway")
    
    # Step 4: Start Flask server
    print("\n[4/5] Starting Flask Server...")
    print("-" * 70)
    
    if os.path.exists("server_patient_doctor.py"):
        print("[•] Flask server starting on http://localhost:5000\n")
        print("Server output:")
        print("=" * 70)
        time.sleep(1)
        
        try:
            subprocess.run([sys.executable, "server_patient_doctor.py"])
        except KeyboardInterrupt:
            print("\n[•] Server stopped by user")
    else:
        print("[X] server_patient_doctor.py not found!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)
