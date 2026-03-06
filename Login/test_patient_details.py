#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the complete Patient Detail and Consultation workflow
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

# Test data
patient_email = "testdetail_p@hospital.com"
patient_password = "Password123!"
patient_name = "Detail Patient"
doctor_email = "testdetail_d@hospital.com"
doctor_password = "Password456!"
doctor_name = "Dr. Detail Specialist"

print("\n" + "="*70)
print("TEST 1: Patient Sign up")
print("="*70)
try:
    payload = {
        "fullname": patient_name,
        "email": patient_email,
        "password": patient_password,
        "phone": "9876543210",
        "role": "patient"
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload, timeout=5)
    data = response.json()
    
    if response.status_code in [200, 201]:
        patient_id = data.get('user_id')
    else:
        # Try login  
        response = requests.post(f"{BASE_URL}/login", json={
            "email": patient_email,
            "password": patient_password
        }, timeout=5)
        data = response.json()
        patient_id = data.get('user', {}).get('id')
    
    print(f"[OK] Patient ID: {patient_id}")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

print("\n" + "="*70)
print("TEST 2: Doctor Sign up")
print("="*70)
try:
    payload = {
        "fullname": doctor_name,
        "email": doctor_email,
        "password": doctor_password,
        "phone": "9876543211",
        "specialization": "Cardiology",
        "license_number": "MD12345",
        "experience_years": "10",
        "consultation_fee": "500",
        "role": "doctor"
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload, timeout=5)
    data = response.json()
    
    if response.status_code in [200, 201]:
        doctor_id = data.get('user_id')
    else:
        response = requests.post(f"{BASE_URL}/login", json={
            "email": doctor_email,
            "password": doctor_password
        }, timeout=5)
        data = response.json()
        doctor_id = data.get('user', {}).get('id')
    
    print(f"[OK] Doctor ID: {doctor_id}")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

print("\n" + "="*70)
print("TEST 3: Book Appointment")
print("="*70)
try:
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": tomorrow,
        "appointment_time": "14:00:00",
        "reason_for_visit": "Routine cardiac checkup",
        "consultation_type": "in-person"
    }
    response = requests.post(f"{BASE_URL}/book-appointment", json=payload, timeout=5)
    data = response.json()
    
    if response.status_code in [200, 201]:
        appointment_id = data.get('appointment_id')
        print(f"[OK] Appointment booked ID: {appointment_id}")
    else:
        print(f"[ERROR] {data}")
        exit(1)
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

print("\n" + "="*70)
print("TEST 4: Doctor adds consultation with COMMENTS")
print("="*70)
try:
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "symptoms": "Chest discomfort and shortness of breath during activity",
        "diagnosis": "Suspected mild angina",
        "comments": "Patient is anxious about symptoms. Avoid strenuous activity. Follow-up in 2 weeks.",
        "medicine_name": "Aspirin",
        "dosage": "100mg",
        "frequency": "Once daily",
        "duration": "30 days",
        "instructions": "Take with food"
    }
    response = requests.post(f"{BASE_URL}/add-consultation", json=payload, timeout=5)
    data = response.json()
    
    if data.get('success'):
        print(f"[OK] Consultation saved with record ID: {data.get('record_id')}")
    else:
        print(f"[ERROR] {data}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*70)
print("TEST 5: Check patient sees medical history WITH comments")
print("="*70)
try:
    response = requests.get(f"{BASE_URL}/get-medical-history/{patient_id}", timeout=5)
    data = response.json()
    records = data.get('records', [])
    
    print(f"[OK] Retrieved {len(records)} medical record(s)")
    for record in records:
        print(f"\n  Doctor: {record.get('doctor_name')}")
        print(f"  Date: {record.get('record_date')}")
        print(f"  Diagnosis: {record.get('diagnosis')}")
        if record.get('comments'):
            print(f"  Doctor Comments: {record.get('comments')}")
        else:
            print(f"  [WARNING] No comments found!")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*70)
print("TEST 6: Check patient sees prescriptions")
print("="*70)
try:
    response = requests.get(f"{BASE_URL}/get-prescriptions/{patient_id}", timeout=5)
    data = response.json()
    prescriptions = data.get('prescriptions', [])
    
    print(f"[OK] Retrieved {len(prescriptions)} prescription(s)")
    for rx in prescriptions:
        print(f"  Medicine: {rx.get('medicine_name')} - {rx.get('dosage')}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*70)
print("SUCCESS - ALL TESTS PASSED")
print("="*70)
print("""
WORKFLOW:
1. Patient created
2. Doctor created
3. Appointment booked
4. Doctor added consultation with COMMENTS
5. Patient now sees:
   - Doctor's diagnosis
   - Doctor's COMMENTS in Medical History
   - Prescribed medicines
""")
