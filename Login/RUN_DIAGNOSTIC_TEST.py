#!/usr/bin/env python3
"""
Comprehensive System Test - Test all components
"""

import requests
import json
import time
import sys

print('='*80)
print('COMPREHENSIVE SYSTEM TEST - Hospital and community Pharmacy management')
print('='*80)
print()

issues = []

# Test 1: Server Health
print('[TEST 1] Server Health Check')
print('-'*80)
try:
    r = requests.get('http://localhost:5000/health', timeout=3)
    print(f'✅ Health endpoint: Status {r.status_code}')
    print(f'   Response: {r.json()}')
except Exception as e:
    print(f'❌ Health check failed: {e}')
    issues.append(f'Health check: {e}')
print()

# Test 2: Static Files
print('[TEST 2] Static File Serving')
print('-'*80)
files = ['login.html', 'signup.html', 'forgot_password.html', 'hospital_landing.html', 'patient_dashboard.html', 'doctor_dashboard.html']
for fname in files:
    try:
        r = requests.get(f'http://localhost:5000/{fname}', timeout=3)
        if r.status_code == 200:
            if 'html' in r.text.lower() or 'script' in r.text.lower():
                print(f'✅ {fname:30} - OK (Status 200)')
            else:
                print(f'⚠️  {fname:30} - Content issue')
                issues.append(f'{fname}: Unexpected content')
        else:
            print(f'❌ {fname:30} - Status {r.status_code}')
            issues.append(f'{fname}: Status {r.status_code}')
    except Exception as e:
        print(f'❌ {fname:30} - Error')
        issues.append(f'{fname}: {str(e)[:50]}')
print()

# Test 3: API URL in HTML Files
print('[TEST 3] Check API_URL Configuration in HTML Files')
print('-'*80)
html_files = ['login.html', 'signup.html', 'forgot_password.html']
for fname in html_files:
    try:
        r = requests.get(f'http://localhost:5000/{fname}', timeout=3)
        content = r.text
        
        search_str = "const API_URL = 'http://localhost:5000'"
        if search_str in content:
            print(f'✅ {fname:30} - API_URL correctly set to localhost:5000')
        elif 'API_URL' in content:
            if 'window.location.protocol' in content:
                print(f'❌ {fname:30} - STILL HAS OLD window.location.protocol logic!')
                issues.append(f'{fname}: Still using old API_URL logic')
            else:
                print(f'⚠️  {fname:30} - Has API_URL but format unclear')
        else:
            print(f'❌ {fname:30} - NO API_URL defined!')
            issues.append(f'{fname}: Missing API_URL')
    except Exception as e:
        print(f'❌ {fname:30} - Error checking: {str(e)[:40]}')
print()

# Test 4: API Endpoints
print('[TEST 4] API Endpoint Availability')
print('-'*80)
endpoints = [
    ('POST', '/login', {'email': 'test@test.com', 'password': 'test'}),
    ('POST', '/signup', {'role': 'patient', 'fullname': 'Test', 'email': f'test{int(time.time())}@test.com', 'phone': '1234567890', 'password': 'test123'}),
    ('GET', '/health', None),
]
for method, endpoint, data in endpoints:
    try:
        if method == 'POST':
            r = requests.post(f'http://localhost:5000{endpoint}', json=data, timeout=3)
        else:
            r = requests.get(f'http://localhost:5000{endpoint}', timeout=3)
        
        print(f'✅ {method:6} {endpoint:20} - Status {r.status_code}')
    except Exception as e:
        print(f'❌ {method:6} {endpoint:20} - Error: {str(e)[:40]}')
        issues.append(f'{method} {endpoint}: {str(e)[:40]}')
print()

# Test 5: CORS Headers
print('[TEST 5] CORS Configuration')
print('-'*80)
try:
    r = requests.options('http://localhost:5000/login', timeout=3)
    cors_header = r.headers.get('Access-Control-Allow-Origin')
    if cors_header == '*' or cors_header:
        print(f'✅ CORS Enabled - Access-Control-Allow-Origin: {cors_header}')
    else:
        print(f'⚠️  CORS header not found in OPTIONS response')
        issues.append('CORS: Header not found')
except Exception as e:
    print(f'❌ CORS check failed: {str(e)[:40]}')
    issues.append(f'CORS check: {str(e)[:40]}')
print()

# Test 6: Database
print('[TEST 6] Database Connection')
print('-'*80)
try:
    import mysql.connector
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='deepanshu')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DATABASE()')
    db = cursor.fetchone()
    print(f'✅ Database connected: {db[0]}')
    
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='deepanshu'")
    tables = cursor.fetchall()
    print(f'✅ Tables found: {len(tables)}')
    for table in tables[:3]:
        print(f'   - {table[0]}')
    if len(tables) > 3:
        print(f'   ... and {len(tables)-3} more')
    
    conn.close()
except Exception as e:
    print(f'❌ Database error: {str(e)[:60]}')
    issues.append(f'Database: {str(e)[:60]}')
print()

# Test 7: Login Flow
print('[TEST 7] Login Flow Test')
print('-'*80)
try:
    # Try login with invalid credentials (should get proper error, not connection error)
    r = requests.post('http://localhost:5000/login', 
                     json={'email': 'invalid@test.com', 'password': 'wrongpass'},
                     timeout=3)
    
    if r.status_code in [200, 401]:
        data = r.json()
        if 'message' in data or 'success' in data:
            print(f'✅ Login endpoint returns proper response (Status {r.status_code})')
        else:
            print(f'⚠️  Login response format unclear: {data}')
    else:
        print(f'❌ Login returned unexpected status: {r.status_code}')
        issues.append(f'Login: Unexpected status {r.status_code}')
except Exception as e:
    print(f'❌ Login flow test failed: {str(e)[:40]}')
    issues.append(f'Login flow: {str(e)[:40]}')
print()

# Summary
print('='*80)
print('TEST SUMMARY')
print('='*80)
if issues:
    print(f'\n⚠️  Found {len(issues)} issue(s):')
    for i, issue in enumerate(issues, 1):
        print(f'   {i}. {issue}')
    sys.exit(1)
else:
    print('\n✅ ALL TESTS PASSED - System is working correctly!')
    print('\n🎉 You can now use the system at:')
    print('   http://localhost:5000/hospital_landing.html')
    sys.exit(0)
