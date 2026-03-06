import requests
from datetime import datetime

BASE = 'http://localhost:5000'

print("\n" + "="*70)
print("HOSPITAL MANAGEMENT SYSTEM - COMPLETE VERIFICATION")
print("="*70)

# Create test accounts
patient_data = {
    'role': 'patient',
    'fullname': 'Debug Patient',
    'email': f'debug_pat_{datetime.now().timestamp()}@test.com',
    'phone': '9999999999',
    'password': 'password123'
}

doctor_data = {
    'role': 'doctor',
    'fullname': 'Dr. Debug',
    'email': f'debug_doc_{datetime.now().timestamp()}@test.com',
    'phone': '888888888',
    'password': 'password123',
    'specialization': 'General Medicine',
    'license_number': 'DLIC001',
    'experience_years': 5,
    'consultation_fee': 500
}

# Create accounts
pr = requests.post(f'{BASE}/signup', json=patient_data)
dr = requests.post(f'{BASE}/signup', json=doctor_data)

patient_id = pr.json()['user_id']
doctor_id = dr.json()['user_id']

print(f"\nTest accounts created:")
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
print(f"\nAppointment booked:")
print(f"  Appointment ID: {appointment_id}")

# Test doctor appointments endpoint with debug info
print(f"\nDEBUG - Testing /get-doctor-appointments/{doctor_id}")
url = f'{BASE}/get-doctor-appointments/{doctor_id}'
r = requests.get(url)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")

if r.status_code != 200:
    print(f"\nERROR DETAILS:")
    try:
        print(r.json())
    except:
        print(r.text)
