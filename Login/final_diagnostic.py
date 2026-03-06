#!/usr/bin/env python3
"""Complete updated diagnostic with correct fields"""
import requests
import json
from datetime import datetime, timedelta
import time

API_BASE = 'http://localhost:5000'

print("\n╔" + "="*58 + "╗")
print("║" + " COMPREHENSIVE SYSTEM DIAGNOSTIC ".center(58) + "║")
print("╚" + "="*58 + "╝\n")

passed = []
failed = []
warnings = []

def test(name, func):
    """Run a test"""
    print(f"Testing: {name}...", end=" ")
    try:
        result = func()
        if result:
            print("✓")
            passed.append(name)
            return result
        else:
            print("✗")
            failed.append(name)
            return None
    except Exception as e:
        print(f"✗ ({str(e)[:50]})")
        failed.append(f"{name}: {e}")
        return None

# Test 1: Server health
def test_server():
    r = requests.get(f'{API_BASE}/health', timeout=3)
    return r.status_code == 200

# Test 2: Patient signup
patient_id = None
def test_patient_signup():
    global patient_id
    r = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Patient',
        'email': f'pat_{time.time()}@test.com',
        'phone': '1234567890',
        'password': 'test123',
        'role': 'patient'
    })
    if r.status_code == 201:
        patient_id = r.json().get('user_id')
        return patient_id is not None
    return False

# Test 3: Doctor signup with ALL required fields
doctor_id = None
def test_doctor_signup():
    global doctor_id
    r = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Doctor',
        'email': f'doc_{time.time()}@test.com',
        'phone': '9876543210',
        'password': 'test123',
        'role': 'doctor',
        'specialization': 'Cardiology',
        'license_number': 'LIC12345678',
        'experience_years': 10,
        'consultation_fee': 500
    })
    if r.status_code == 201:
        doctor_id = r.json().get('user_id')
        return doctor_id is not None
    else:
        print(f"\n  Error: {r.json()}")
    return False

# Test 4: Pharmacist signup
pharmacist_id = None
def test_pharmacist_signup():
    global pharmacist_id
    r = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Pharmacist',
        'email': f'pharm_{time.time()}@test.com',
        'phone': '5555555555',
        'password': 'test123',
        'role': 'pharmacist'
    })
    if r.status_code == 201:
        pharmacist_id = r.json().get('user_id')
        return pharmacist_id is not None
    return False

# Test 5: Admin signup
admin_id = None
def test_admin_signup():
    global admin_id
    r = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Admin',
        'email': f'admin_{time.time()}@test.com',
        'phone': '4444444444',
        'password': 'test123',
        'role': 'admin'
    })
    if r.status_code == 201:
        admin_id = r.json().get('user_id')
        return admin_id is not None
    return False

# Test 6: Add medicine
medicine_id = None
def test_add_medicine():
    global medicine_id
    if not admin_id:
        print("\n  Skipped (no admin)")
        return None
    r = requests.post(f'{API_BASE}/api/medicines', json={
        'actor_id': admin_id,
        'name': 'Test Med',
        'manufacturer': 'TestCorp',
        'batch_no': 'BATCH001',
        'quantity': 100,
        'unit_price': 50.0,
        'expiry_date': '2026-12-31'
    })
    if r.status_code == 201:
        medicine_id = r.json().get('medicine_id')
        return medicine_id is not None
    return False

# Test 7: Book appointment with correct fields
appointment_id = None
def test_book_appointment():
    global appointment_id
    if not (patient_id and doctor_id):
        print(f"\n  Skipped (patient_id={patient_id}, doctor_id={doctor_id})")
        return None
    r = requests.post(f'{API_BASE}/book-appointment', json={
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'appointment_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'appointment_time': '10:00',
        'reason_for_visit': 'Checkup',
        'consultation_type': 'in-person'
    })
    if r.status_code in [200, 201]:
        data = r.json()
        appointment_id = data.get('appointment_id')
        return appointment_id is not None
    else:
        print(f"\n  Error: {r.json()}")
    return False

# Test 8: Add consultation
def test_add_consultation():
    if not (doctor_id and medicine_id and appointment_id):
        print(f"\n  Skipped (doctor={doctor_id}, med={medicine_id}, apt={appointment_id})")
        return None
    r = requests.post(f'{API_BASE}/add-consultation', json={
        'doctor_id': doctor_id,
        'appointment_id': appointment_id,
        'medicine_id': medicine_id,
        'quantity': 5,
        'diagnosis': 'Test diagnosis',
        'notes': 'Test notes'
    })
    return r.status_code in [200, 201]

# Test 9: Restock request
def test_restock_request():
    if not (pharmacist_id and medicine_id):
        print(f"\n  Skipped (pharm={pharmacist_id}, med={medicine_id})")
        return None
    r = requests.post(f'{API_BASE}/api/restock-request', json={
        'actor_id': pharmacist_id,
        'medicine_id': medicine_id,
        'medicine_name': 'Test Med',
        'requested_quantity': 50,
        'reason': 'Low stock'
    })
    return r.status_code == 201

# Test 10: Admin stats
def test_admin_stats():
    if not admin_id:
        print("\n  Skipped (no admin)")
        return None
    r = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
    return r.status_code == 200

# Test 11: Portal rendering
def test_portals():
    portals = ['/login.html', '/admin_portal.html', '/patient_dashboard.html', '/doctor_dashboard.html']
    all_ok = True
    for p in portals:
        r = requests.get(f'{API_BASE}{p}', timeout=3)
        if r.status_code != 200:
            print(f"\n  Failed: {p} ({r.status_code})")
            all_ok = False
    return all_ok

# Run all tests
test("Server health", test_server)
test("Patient signup", test_patient_signup)
test("Doctor signup (with full fields)", test_doctor_signup)
test("Pharmacist signup", test_pharmacist_signup)
test("Admin signup", test_admin_signup)
test("Add medicine", test_add_medicine)
test("Book appointment", test_book_appointment)
test("Add consultation", test_add_consultation)
test("Restock request", test_restock_request)
test("Admin stats", test_admin_stats)
test("Portal rendering", test_portals)

# Summary
print("\n" + "="*60)
print("DIAGNOSTIC SUMMARY")
print("="*60)
print(f"✓ Passed: {len(passed)}")
print(f"✗ Failed: {len(failed)}")
if failed:
    for f in failed:
        print(f"  - {f}")
else:
    print("\n✓ ALL SYSTEMS OPERATIONAL!")
