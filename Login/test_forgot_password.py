#!/usr/bin/env python3
"""
Forgot Password Testing Script
Tests the complete forgot password workflow
"""

import mysql.connector
import requests
import time
import json

# Configuration
API_URL = 'http://localhost:5000'
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

def test_forgot_password_flow():
    """Test complete forgot password workflow"""
    
    print("=" * 70)
    print("🔒 FORGOT PASSWORD WORKFLOW TEST")
    print("=" * 70)
    
    try:
        # Step 1: Ensure server is running
        print("\n1️⃣  Checking server connection...")
        try:
            response = requests.get(f'{API_URL}/health', timeout=2)
            if response.status_code == 200:
                print("   ✅ Server is running at", API_URL)
            else:
                print("   ⚠️  Server response unclear")
        except:
            print("   ❌ Server not running. Start it with: python server_patient_doctor.py")
            return
        
        # Step 2: Create test user
        print("\n2️⃣  Creating test user...")
        test_email = 'forgotpasstest@hospital.com'
        test_password = 'oldpassword123'
        
        # Clean up if exists
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM login WHERE email = %s", (test_email,))
        conn.commit()
        
        # Create new user
        import bcrypt
        hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute('''
            INSERT INTO login (full_name, email, phone, password, role)
            VALUES (%s, %s, %s, %s, %s)
        ''', ('Test User', test_email, '+91-9876543210', hashed, 'patient'))
        conn.commit()
        print(f"   ✅ Test user created: {test_email}")
        
        # Step 3: Test forgot password request
        print("\n3️⃣  Testing forgot password request...")
        try:
            response = requests.post(
                f'{API_URL}/forgot-password',
                json={'email': test_email},
                timeout=5
            )
            data = response.json()
            
            if response.status_code == 200 and data.get('success'):
                temp_password = data.get('temp_password')
                print(f"   ✅ Forgot password request successful")
                print(f"   📝 Temporary Password: {temp_password}")
                
                # Step 4: Test password reset
                print("\n4️⃣  Testing password reset...")
                new_password = 'newpassword456'
                
                response = requests.post(
                    f'{API_URL}/reset-password',
                    json={
                        'email': test_email,
                        'temp_password': temp_password,
                        'new_password': new_password
                    },
                    timeout=5
                )
                data = response.json()
                
                if response.status_code == 200 and data.get('success'):
                    print(f"   ✅ Password reset successful")
                    
                    # Step 5: Verify new password works
                    print("\n5️⃣  Verifying new password works for login...")
                    response = requests.post(
                        f'{API_URL}/login',
                        json={'email': test_email, 'password': new_password},
                        timeout=5
                    )
                    
                    if response.status_code == 200 and response.json().get('success'):
                        print(f"   ✅ Login with new password successful")
                        
                        # Step 6: Verify old password doesn't work
                        print("\n6️⃣  Verifying old password no longer works...")
                        response = requests.post(
                            f'{API_URL}/login',
                            json={'email': test_email, 'password': test_password},
                            timeout=5
                        )
                        
                        if response.status_code == 401:
                            print(f"   ✅ Old password correctly rejected")
                            
                            print("\n" + "=" * 70)
                            print("✅ ALL FORGOT PASSWORD TESTS PASSED!")
                            print("=" * 70)
                            print("\n📊 SUMMARY:")
                            print("   ✅ Forgot password request")
                            print("   ✅ Temporary password generation")
                            print("   ✅ Password reset with temp password")
                            print("   ✅ Login with new password")
                            print("   ✅ Old password invalidated")
                            print("\n🎉 Forgot Password Feature is FULLY OPERATIONAL!")
                            
                        else:
                            print(f"   ❌ Old password should be rejected")
                    else:
                        print(f"   ❌ New password login failed")
                else:
                    print(f"   ❌ Password reset failed: {data.get('message')}")
            else:
                print(f"   ❌ Forgot password request failed: {data.get('message')}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ API request failed: {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Test Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n🛠️  BEFORE RUNNING THIS TEST:")
    print("   1. Make sure the server is running")
    print("   2. MySQL must be running")
    print("   3. Ports 5000 and 3306 must be accessible")
    print("\n   Starting test in 2 seconds...\n")
    time.sleep(2)
    
    test_forgot_password_flow()
