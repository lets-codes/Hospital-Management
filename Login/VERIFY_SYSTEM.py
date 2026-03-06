#!/usr/bin/env python3
"""Complete system test - verify all systems working"""

import requests
from datetime import datetime

BASE = 'http://localhost:5000'

print("\n" + "="*70)
print("HOSPITAL MANAGEMENT SYSTEM - COMPLETE VERIFICATION")
print("="*70)

# Create test accounts
patient_data = {
    'role': 'patient',
    'fullname': 'Verification Patient',
    'email': f'verify_pat_{datetime.now().timestamp()}@test.com',
    'phone': '9999999999',
    'password': 'password123'
}

doctor_data = {
    'role': 'doctor',
    'fullname': 'Dr. Verification',
    'email': f'verify_doc_{datetime.now().timestamp()}@test.com',
    'phone': '8888888888',
    'password': 'password123',
    'specialization': 'General Medicine',
    'license_number': 'VLIC001',
    'experience_years': 5,
    'consultation_fee': 500
}

# Create accounts
pr = requests.post(f'{BASE}/signup', json=patient_data)
dr = requests.post(f'{BASE}/signup', json=doctor_data)

patient_id = pr.json()['user_id']
doctor_id = dr.json()['user_id']

print(f"\n✓ Test accounts created:")
print(f"  Patient ID: {patient_id}")
print(f"  Doctor ID: {doctor_id}")

# Book appointment
appt_data = {
    'patient_id': patient_id,
    'doctor_id': doctor_id,
    'appointment_date': '2026-02-18',
    'appointment_time': '14:00',
    'reason_for_visit': 'Checkup',
    'consultation_type': 'in-person'
}
appt_r = requests.post(f'{BASE}/book-appointment', json=appt_data)
appointment_id = appt_r.json()['appointment_id']
print(f"\n✓ Appointment booked:")
print(f"  Appointment ID: {appointment_id}")

# Test doctor API endpoints
print(f"\n✓ Doctor Dashboard Endpoints:")
tests = [
    (f'{BASE}/get-doctor-appointments/{doctor_id}', 'GET Doctor Appointments'),
    (f'{BASE}/get-doctor-patients/{doctor_id}', 'GET Doctor Patients'),
    (f'{BASE}/get-doctors', 'GET Doctors List'),
    (f'{BASE}/get-patient-details/{patient_id}', 'GET Patient Details'),
    (f'{BASE}/get-patient-appointments/{patient_id}', 'GET Patient Appointments'),
]

failed = False
for url, desc in tests:
    r = requests.get(url)
    status = f"✓ {r.status_code}" if r.status_code == 200 else f"✗ {r.status_code}"
    print(f"  {status} - {desc}")
    if r.status_code != 200:
        failed = True

# Test new features
print(f"\n✓ New Features Endpoints:")
features = [
    (f'{BASE}/api/lab-results/{patient_id}', 'GET Lab Results'),
    (f'{BASE}/api/alerts/{patient_id}', 'GET Alerts'),
    (f'{BASE}/api/followups/{patient_id}', 'GET Follow-ups'),
]

for url, desc in features:
    r = requests.get(url)
    status = f"✓ {r.status_code}" if r.status_code == 200 else f"✗ {r.status_code}"
    print(f"  {status} - {desc}")
    if r.status_code != 200:
        failed = True

print("\n" + "="*70)
if not failed:
    print("SUCCESS: ALL SYSTEMS OPERATIONAL!")
    print("="*70)
    print("\nDoctor Dashboard Instructions:")
    print("1. Open browser: http://localhost:5000/doctor_dashboard.html")
    print(f"2. Login with:")
    print(f"   Email: {doctor_data['email']}")
    print(f"   Password: {doctor_data['password']}")
    print("3. All tabs and options should now work normally")
    print("4. Click on any tab to view data and features")
    print("="*70 + "\n")
else:
    print("SOME TESTS FAILED - CHECK SERVER LOGS")
    print("="*70 + "\n")
