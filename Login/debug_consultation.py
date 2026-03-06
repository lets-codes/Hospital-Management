#!/usr/bin/env python3
"""Debug add-consultation endpoint"""
import requests
import time
from datetime import datetime, timedelta

API_BASE = 'http://localhost:5000'

# Create patient
p = requests.post(f'{API_BASE}/signup', json={
    'fullname': 'PTest',
    'email': f'p_{time.time()}@t.com',
    'phone': '111111',
    'password': 'ptest123',
    'role': 'patient'
})
print(f"Patient: {p.status_code}")
if p.status_code != 201:
    print(f"  Error: {p.json()}")
    exit(1)
pid = p.json()['user_id']

# Create doctor
d = requests.post(f'{API_BASE}/signup', json={
    'fullname': 'DTest',
    'email': f'd_{time.time()}@t.com',
    'phone': '222222',
    'password': 'dtest123',
    'role': 'doctor',
    'specialization': 'GP',
    'license_number': 'LIC123',
    'experience_years': 5,
    'consultation_fee': 100
})
print(f"Doctor: {d.status_code}")
if d.status_code != 201:
    print(f"  Error: {d.json()}")
    exit(1)
did = d.json()['user_id']

# Book appointment
a = requests.post(f'{API_BASE}/book-appointment', json={
    'patient_id': pid,
    'doctor_id': did,
    'appointment_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    'appointment_time': '10:00',
    'reason_for_visit': 'test'
})
print(f"Appointment: {a.status_code}")
if a.status_code not in [200, 201]:
    print(f"  Error: {a.json()}")
    exit(1)
aid = a.json()['appointment_id']

# Test add-consultation
print("\n" + "="*60)
print("TESTING ADD-CONSULTATION")
print("="*60)
r = requests.post(f'{API_BASE}/add-consultation', json={
    'patient_id': pid,
    'doctor_id': did,
    'symptoms': 'test symptoms',
    'diagnosis': 'test diagnosis',
    'medicine_name': 'TestMedicine',
    'dosage': '1 tablet',
    'frequency': 'Twice daily',
    'duration': '7 days',
    'instructions': 'take with water'
})
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")
if r.status_code == 200:
    print("\n✓ SUCCESS - Add consultation is working!")
else:
    print(f"\n✗ FAILED - Error in add-consultation")
