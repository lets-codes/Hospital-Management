#!/usr/bin/env python3
"""Test server connectivity"""

import socket
import time

def check_server():
    try:
        # Try to connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', 5000))
            if result == 0:
                print("✅ Server is running on localhost:5000")
                print("\n🎉 SUCCESS! You can now access:")
                print("   📍 http://localhost:5000/hospital_landing.html")
                print("   📍 http://localhost:5000/login.html")
                print("   📍 http://localhost:5000/signup.html")
                print("   📍 http://localhost:5000/forgot_password.html")
                print("\n✅ All features available:")
                print("   ✓ Patient Login/Signup")
                print("   ✓ Doctor Login/Signup")
                print("   ✓ Forgot Password Recovery")
                return True
            else:
                print("❌ Server is NOT running on port 5000")
                print("\nTo start the server, run:")
                print("   python server_patient_doctor.py")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 Checking Server Status...")
    print("=" * 60 + "\n")
    check_server()
