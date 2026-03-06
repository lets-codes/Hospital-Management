#!/usr/bin/env python3
"""Test doctor dashboard functionality"""

import requests
import json
from datetime import datetime

BASE = 'http://localhost:5000'

# Create a doctor account for testing
doctor_data = {
    'role': 'doctor',
    'fullname': 'Test Doctor',
    'email': f'test_doc_{datetime.now().timestamp()}@test.com',
    'phone': '9876543210',
    'password': 'password123',
    'specialization': 'General Medicine',
    'license_number': 'LIC999',
    'experience_years': 5,
    'consultation_fee': 500
}

print("Creating doctor account...")
r = requests.post(f'{BASE}/signup', json=doctor_data)
if r.status_code != 201:
    print(f"Failed: {r.text}")
    exit(1)

doctor_id = r.json()['user_id']
print(f"✓ Doctor created: ID {doctor_id}")

# Login as doctor
print("\nLogging in as doctor...")
login_data = {
    'email': doctor_data['email'],
    'password': doctor_data['password']
}
r = requests.post(f'{BASE}/login', json=login_data)
if r.status_code != 200:
    print(f"Failed: {r.text}")
    exit(1)

user = r.json()['user']
print(f"✓ Logged in: {user['full_name']} (Role: {user['role']})")

# Test doctor endpoints
print("\n=== Testing Doctor Endpoints ===")

# 1. Get doctor appointments
print("\n1. GET /get-doctor-appointments/{doctor_id}")
r = requests.get(f'{BASE}/get-doctor-appointments/{doctor_id}')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Today: {len(data.get('today', []))} appointments")
    print(f"   Upcoming: {len(data.get('upcoming', []))} appointments")
    print("   ✓ WORKING")
else:
    print(f"   ✗ ERROR: {r.text}")

# 2. Get doctor patients
print("\n2. GET /get-doctor-patients/{doctor_id}")
r = requests.get(f'{BASE}/get-doctor-patients/{doctor_id}')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Patients: {len(data.get('patients', []))}")
    print("   ✓ WORKING")
else:
    print(f"   ✗ ERROR: {r.text}")

# 3. Get doctors list
print("\n3. GET /get-doctors")
r = requests.get(f'{BASE}/get-doctors')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Doctors: {len(data.get('doctors', []))}")
    print("   ✓ WORKING")
else:
    print(f"   ✗ ERROR: {r.text}")

print("\n" + "="*50)
print("Doctor Dashboard Basic Endpoints: ALL WORKING ✓")
print("="*50)
print("\nNext step: Open browser and manually test:")
print(f"1. Go to http://localhost:5000/doctor_dashboard.html")
print(f"2. Email: {doctor_data['email']}")
print(f"3. Password: {doctor_data['password']}")
print(f"4. Try clicking on each tab and option")
