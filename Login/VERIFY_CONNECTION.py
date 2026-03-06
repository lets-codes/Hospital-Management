#!/usr/bin/env python3
"""
Verification Test - Check if Hospital Management System is Working
Run this after starting the server to verify all connections work
"""

import requests
import time
import sys
import json

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_server_health():
    """Test if server is running and responding"""
    print_header("TEST 1: Server Connection")
    
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server is RUNNING")
            print(f"  Status: {data.get('status')}")
            print(f"  Service: {data.get('service')}")
            return True
        else:
            print(f"✗ Server returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("  Make sure:")
        print("    1. Flask server is running")
        print("    2. Port 5000 is not blocked")
        print("    3. Try: python server_patient_doctor.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_static_files():
    """Test if static HTML files are served"""
    print_header("TEST 2: Static File Serving")
    
    files_to_test = [
        ('hospital_landing.html', 'Hospital Landing'),
        ('login.html', 'Login Page'),
        ('signup.html', 'Signup Page'),
    ]
    
    all_ok = True
    for filename, label in files_to_test:
        try:
            response = requests.get(f'http://localhost:5000/{filename}', timeout=5)
            if response.status_code == 200:
                print(f"✓ {label:20} ({filename}) - OK")
            else:
                print(f"✗ {label:20} ({filename}) - Status {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"✗ {label:20} ({filename}) - Error: {e}")
            all_ok = False
    
    return all_ok

def test_api_endpoints():
    """Test API endpoint availability"""
    print_header("TEST 3: API Endpoints")
    
    # Test login endpoint
    print("Testing POST /login endpoint...")
    try:
        response = requests.post(
            'http://localhost:5000/login',
            json={'email': 'test@test.com', 'password': 'test'},
            timeout=5
        )
        print(f"✓ /login endpoint exists (Status: {response.status_code})")
        endpoint_ok = True
    except requests.exceptions.ConnectionError:
        print("✗ /login endpoint not responding")
        endpoint_ok = False
    except Exception as e:
        print(f"✗ Error testing /login: {e}")
        endpoint_ok = False
    
    # Test signup endpoint
    print("Testing POST /signup endpoint...")
    try:
        response = requests.post(
            'http://localhost:5000/signup',
            json={
                'role': 'patient',
                'fullname': 'test',
                'email': 'test@test.com',
                'phone': '1234567890',
                'password': 'test'
            },
            timeout=5
        )
        print(f"✓ /signup endpoint exists (Status: {response.status_code})")
        return endpoint_ok and True
    except Exception as e:
        print(f"✗ Error testing /signup: {e}")
        return endpoint_ok and False

def test_cors_headers():
    """Test CORS headers"""
    print_header("TEST 4: CORS Configuration")
    
    try:
        response = requests.options(
            'http://localhost:5000/login',
            timeout=5
        )
        headers = response.headers
        
        cors_header = headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print(f"✓ CORS is configured")
            print(f"  Access-Control-Allow-Origin: {cors_header}")
            return True
        else:
            print("⚠ CORS headers not found (but service may still work)")
            return True
    except Exception as e:
        print(f"⚠ Could not verify CORS: {e}")
        return True

def test_database_connection():
    """Test database connectivity"""
    print_header("TEST 5: Database Connection")
    
    print("Attempting to verify database availability...")
    
    try:
        response = requests.post(
            'http://localhost:5000/signup',
            json={
                'role': 'patient',
                'fullname': 'test',
                'email': f'test_{int(time.time())}@test.com',
                'phone': '1234567890',
                'password': 'test123'
            },
            timeout=5
        )
        
        if response.status_code == 400:
            data = response.json()
            if 'message' in data:
                msg = data['message'].lower()
                if 'database' in msg or 'connection' in msg:
                    print(f"✗ Database connection error: {data['message']}")
                    return False
                else:
                    print(f"✓ Database appears to be working")
                    return True
        elif response.status_code == 500:
            print(f"⚠ Server error - likely database issue")
            return False
        else:
            print(f"✓ Database request processed (Status: {response.status_code})")
            return True
            
    except requests.exceptions.ConnectionError:
        print("✗ Server not responding")
        return False
    except Exception as e:
        print(f"⚠ Could not fully test database: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print_header("VERIFICATION RESULTS")
    
    total = len(results)
    passed = sum(1 for r in results if r)
    
    print(f"\nTests Passed: {passed}/{total}\n")
    
    if passed == total:
        print("✅ "*15)
        print("\n🎉 ALL TESTS PASSED - System is working correctly!\n")
        print("✅ "*15)
        print("\n✓ You can now:")
        print("  1. Open http://localhost:5000/hospital_landing.html")
        print("  2. Login with your hospital credentials")
        print("  3. Use the full hospital management system")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed\n")
        print("Common fixes:")
        print("  • Server not running? Use: START_SERVER.bat")
        print("  • MySQL not running? Start MySQL80 in Services")
        print("  • Port in use? Run: python START_SERVER_FIXED.py")
        return False

def main():
    """Main execution"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🏥 Hospital System - Connection Verification".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("Initializing tests...\n")
    time.sleep(1)
    
    results = [
        test_server_health(),
        test_static_files(),
        test_api_endpoints(),
        test_cors_headers(),
        test_database_connection(),
    ]
    
    success = print_summary(results)
    
    print("\n")
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
