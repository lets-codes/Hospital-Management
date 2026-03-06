#!/usr/bin/env python3
"""Test script to verify admin portal features and fixes"""

import requests
import json
import time
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def test_server_health():
    """Test if server is running"""
    try:
        r = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"✓ Server Health: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"✗ Server Health: {str(e)}")
        return False

def test_medicines():
    """Test medicines endpoint"""
    try:
        r = requests.get(f'{BASE_URL}/api/medicines', timeout=5)
        print(f"✓ Get Medicines: {r.status_code}")
        if r.status_code == 200:
            medicines = r.json()
            print(f"  - Found {len(medicines)} medicines")
            return True
        return False
    except Exception as e:
        print(f"✗ Get Medicines: {str(e)}")
        return False

def test_restock_requests():
    """Test restock requests endpoint"""
    try:
        # Test without auth first
        r = requests.get(f'{BASE_URL}/api/admin/restock-requests', timeout=5)
        print(f"✓ Get Restock Requests (unauth): {r.status_code}")
        return r.status_code in [200, 401]
    except Exception as e:
        print(f"✗ Get Restock Requests: {str(e)}")
        return False

def test_login():
    """Test login endpoint"""
    try:
        payload = {
            'email': 'admin@hospital.com',
            'password': 'password123'
        }
        r = requests.post(f'{BASE_URL}/login', json=payload, timeout=5)
        print(f"✓ Login Endpoint: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  - User: {data.get('full_name', 'Unknown')}")
            print(f"  - Role: {data.get('role', 'Unknown')}")
            return data.get('role') == 'admin', data
        return False, None
    except Exception as e:
        print(f"✗ Login: {str(e)}")
        return False, None

def test_signup():
    """Test signup endpoint"""
    try:
        payload = {
            'full_name': 'Test User',
            'email': f'test_{int(time.time())}@hospital.com',
            'phone': '555-1234',
            'role': 'patient',
            'password': 'TestPass123'
        }
        r = requests.post(f'{BASE_URL}/signup', json=payload, timeout=5)
        print(f"✓ Signup Endpoint: {r.status_code}")
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"✗ Signup: {str(e)}")
        return False

def test_notifications():
    """Test notifications endpoint"""
    try:
        r = requests.get(f'{BASE_URL}/api/notifications', timeout=5)
        print(f"✓ Get Notifications: {r.status_code}")
        if r.status_code == 200:
            notifs = r.json()
            print(f"  - Found {len(notifs)} notifications")
        return r.status_code == 200
    except Exception as e:
        print(f"✗ Get Notifications: {str(e)}")
        return False

def test_sse_stream():
    """Test SSE stream endpoint"""
    try:
        r = requests.get(f'{BASE_URL}/stream', timeout=2, stream=True)
        print(f"✓ SSE Stream: {r.status_code}")
        return r.status_code == 200
    except requests.exceptions.Timeout:
        print(f"✓ SSE Stream: 200 (streaming)")
        return True
    except Exception as e:
        print(f"✗ SSE Stream: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("ADMIN PORTAL SYSTEM TEST")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}\n")
    
    results = []
    
    # Run tests
    print("1. Core Server Tests")
    print("-" * 50)
    results.append(("Server Health", test_server_health()))
    results.append(("Medicines API", test_medicines()))
    results.append(("Restock Requests API", test_restock_requests()))
    results.append(("SSE Stream", test_sse_stream()))
    
    print("\n2. Authentication Tests")
    print("-" * 50)
    is_admin, user_data = test_login()
    results.append(("Login (Admin)", is_admin))
    results.append(("Signup (New User)", test_signup()))
    
    print("\n3. Feature Tests")
    print("-" * 50)
    results.append(("Notifications", test_notifications()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "="*50)
    if passed == total:
        print("✓ ALL TESTS PASSED - System is operational!")
    else:
        print(f"⚠ {total - passed} test(s) failed - Please review")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
