#!/usr/bin/env python3
"""Test appointment deletion feature"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def test_appointment_deletion():
    print("Testing Appointment Deletion Feature")
    print("=" * 60)
    
    # Set up test data
    patient_id = 1  # First patient
    doctor_id = 1   # First doctor
    appointment_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    appointment_time = "10:00"
    reason = "Routine checkup"
    
    # Step 1: Book an appointment
    print("\n[1] Booking a test appointment...")
    book_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'appointment_date': appointment_date,
        'appointment_time': appointment_time,
        'reason_for_visit': reason
    }
    
    response = requests.post(f"{BASE_URL}/book-appointment", json=book_data)
    if response.status_code == 201:
        appointment = response.json().get('appointment', {})
        appointment_id = appointment.get('id')
        print(f"✓ Appointment booked successfully (ID: {appointment_id})")
    else:
        print(f"✗ Failed to book appointment: {response.status_code}")
        print(response.json())
        return False
    
    # Step 2: Get appointments to confirm it was created
    print(f"\n[2] Fetching patient appointments...")
    response = requests.get(f"{BASE_URL}/get-patient-appointments/{patient_id}")
    if response.status_code == 200:
        appointments = response.json().get('appointments', [])
        print(f"✓ Found {len(appointments)} appointments")
        app_found = any(a['id'] == appointment_id for a in appointments)
        if app_found:
            print(f"✓ Newly booked appointment (ID: {appointment_id}) is in the list")
        else:
            print(f"✗ Could not find newly booked appointment")
            return False
    else:
        print(f"✗ Failed to fetch appointments: {response.status_code}")
        return False
    
    # Step 3: Delete the appointment
    print(f"\n[3] Deleting appointment (ID: {appointment_id})...")
    delete_data = {'patient_id': patient_id}
    response = requests.delete(f"{BASE_URL}/delete-appointment/{appointment_id}", json=delete_data)
    if response.status_code == 200:
        print(f"✓ Appointment deleted successfully")
        print(f"   Response: {response.json()}")
    else:
        print(f"✗ Failed to delete appointment: {response.status_code}")
        print(response.json())
        return False
    
    # Step 4: Verify appointment is gone
    print(f"\n[4] Verifying appointment was deleted...")
    response = requests.get(f"{BASE_URL}/get-patient-appointments/{patient_id}")
    if response.status_code == 200:
        appointments = response.json().get('appointments', [])
        app_found = any(a['id'] == appointment_id for a in appointments)
        if not app_found:
            print(f"✓ Appointment successfully removed from patient's list")
        else:
            print(f"✗ Appointment still exists in patient's list")
            return False
    else:
        print(f"✗ Failed to fetch appointments: {response.status_code}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)
    print("\nFeature working correctly!")
    print("Patients can now delete appointments by:")
    print("1. Clicking on a scheduled appointment row, or")
    print("2. Clicking the 'Delete' button in the appointment row")
    return True

if __name__ == "__main__":
    test_appointment_deletion()
