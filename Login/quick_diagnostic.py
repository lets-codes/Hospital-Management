#!/usr/bin/env python3
"""Quick diagnostic to find issues"""
import requests
import json
from datetime import datetime, timedelta
import time

API_BASE = 'http://localhost:5000'
issues = []
warnings = []

# 1. Test server
try:
    r = requests.get(f'{API_BASE}/health', timeout=3)
    print(f"✓ Server responding")
except:
    print("✗ Server not responding")
    exit(1)

# 2. Test doctor signup (known issue)
resp = requests.post(f'{API_BASE}/signup', json={
    'fullname': 'Test Doctor',
    'email': f'doc_{time.time()}@test.com',
    'phone': '1234567890',
    'password': 'test123',
    'role': 'doctor',
    'specialization': 'General'
})
print(f"Doctor signup: {resp.status_code}")
if resp.status_code != 201:
    print(f"  ERROR: {resp.json()}")
    issues.append("Doctor signup missing required fields (license_number, experience_years)")

# 3. Test patient signup
resp = requests.post(f'{API_BASE}/signup', json={
    'fullname': 'Test Patient',
    'email': f'pat_{time.time()}@test.com',
    'phone': '1234567890',
    'password': 'test123',
    'role': 'patient'
})
patient_id = resp.json().get('user_id') if resp.status_code == 201 else None
print(f"Patient signup: {'OK' if patient_id else 'FAIL'}")

# 4. Test portal rendering
portals = ['/login.html', '/admin_portal.html', '/patient_dashboard.html']
for p in portals:
    resp = requests.get(f'{API_BASE}{p}')
    status = "✓" if resp.status_code == 200 else "✗"
    print(f"{status} {p}")

print("\n" + "="*60)
if issues:
    print(f"ISSUES FOUND: {len(issues)}")
    for i in issues:
        print(f"  - {i}")
else:
    print("✓ No critical issues detected")
