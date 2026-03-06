#!/usr/bin/env python3
"""
Comprehensive System Diagnostic for Hospital Management System
Tests all major endpoints and identifies issues
"""
import requests
import json
import sys
import time
from datetime import datetime

BASE_URL = 'http://localhost:5000'
ISSUES = []
SUCCESSES = []

def test_endpoint(method, endpoint, data=None, expected_status=None, name=""):
    """Test an API endpoint and log results"""
    try:
        url = f"{BASE_URL}{endpoint}"
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'}, timeout=5)
        else:
            return None
        
        status = response.status_code
        success = True if expected_status is None else (status == expected_status)
        
        result = {
            'name': name or f"{method} {endpoint}",
            'method': method,
            'endpoint': endpoint,
            'status': status,
            'success': success,
            'data': response.json() if response.text else None
        }
        
        if success:
            SUCCESSES.append(result)
            print(f"✓ {result['name']}: {status}")
        else:
            ISSUES.append(result)
            print(f"✗ {result['name']}: {status}")
        
        return result
    except Exception as e:
        ISSUES.append({
            'name': name or f"{method} {endpoint}",
            'error': str(e)
        })
        print(f"✗ {name or f'{method} {endpoint}'}: {str(e)}")
        return None

print("\n" + "="*70)
print("COMPREHENSIVE SYSTEM DIAGNOSTIC")
print("="*70)

print("\n[1] Checking server health...")
test_endpoint('GET', '/health', name="Server Health")

print("\n[2] Testing authentication endpoints...")
# Use a unique email per run to avoid 409 conflicts from repeated tests
TEST_EMAIL = f"test_patient_{int(time.time())}@test.local"
test_endpoint('POST', '/signup', data={
    'fullname': 'Test Patient',
    'email': TEST_EMAIL,
    'phone': '9999999999',
    'password': 'password123',
    'role': 'patient'
}, expected_status=201, name="Patient Signup")

test_endpoint('POST', '/login', data={
    'email': TEST_EMAIL,
    'password': 'password123'
}, name="Patient Login")

print("\n[3] Testing medicine endpoints...")
test_endpoint('GET', '/api/medicines', name="Get Medicines List")

print("\n[4] Testing pharmacist endpoints...")
test_endpoint('GET', '/api/pharmacist/inventory?actor_id=1', name="Pharmacist Inventory")

print("\n[5] Testing admin endpoints...")
test_endpoint('GET', '/api/admin/settings', name="Admin Settings")

test_endpoint('GET', '/api/admin/users?actor_id=1', name="Admin Users (requires admin role)")

test_endpoint('GET', '/api/admin/restock-requests?actor_id=1', name="Admin Restock Requests")

print("\n[6] Testing appointments (patient)...")
test_endpoint('POST', '/book-appointment', data={
    'patient_id': 1,
    'doctor_id': 1,
    'appointment_date': '2026-02-20',
    'appointment_time': '10:00',
    'reason_for_visit': 'Checkup'
}, name="Book Appointment")

print("\n[7] Testing notifications...")
test_endpoint('GET', '/api/notifications?role=admin&limit=10', name="Get Notifications")

print("\n[8] Testing SSE stream...")
try:
    response = requests.get(f"{BASE_URL}/stream", timeout=2, stream=True)
    if response.status_code == 200:
        SUCCESSES.append({'name': 'SSE Stream', 'status': 200})
        print(f"✓ SSE Stream: {response.status_code}")
    else:
        ISSUES.append({'name': 'SSE Stream', 'status': response.status_code})
        print(f"✗ SSE Stream: {response.status_code}")
except Exception as e:
    ISSUES.append({'name': 'SSE Stream', 'error': str(e)})
    print(f"✗ SSE Stream: {str(e)}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"✓ Successful Tests: {len(SUCCESSES)}")
print(f"✗ Issues Found: {len(ISSUES)}")

if ISSUES:
    print("\nDETailed Issues:")
    for issue in ISSUES:
        print(f"  - {issue.get('name', 'Unknown')}: {issue.get('error', issue.get('status', 'Unknown error'))}")

print("\n✓ Successful Endpoints:")
for success in SUCCESSES:
    print(f"  - {success['name']}")

print("\n" + "="*70)
