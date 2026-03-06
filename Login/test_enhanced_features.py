#!/usr/bin/env python3
"""
Test Enhanced Features:
- Lab Results
- Patient Alerts
- Follow-up Scheduling
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000'

def create_test_accounts():
    """Create test patient and doctor accounts"""
    print("\n=== STEP 1: Creating Test Accounts ===")
    
    # Create test patient
    patient_data = {
        'fullname': 'Test Patient Enhanced',
        'email': f'test_enhanced_{datetime.now().timestamp()}@patient.com',
        'password': 'Test@123',
        'phone': '9999999999',
        'role': 'patient'
    }
    
    patient_response = requests.post(f'{BASE_URL}/signup', json=patient_data)
    if patient_response.status_code != 201:
        print(f"FAILED to create patient: {patient_response.text}")
        return None, None
    
    patient_json = patient_response.json()
    patient_id = patient_json.get('user_id')
    if not patient_id:
        print(f"FAILED: No user_id in response: {patient_json}")
        return None, None
    print(f"OK - Patient created (ID: {patient_id})")
    
    # Create test doctor
    doctor_data = {
        'fullname': 'Dr. Enhanced Features',
        'email': f'test_enhanced_doc_{datetime.now().timestamp()}@doctor.com',
        'password': 'Doc@123',
        'phone': '8888888888',
        'role': 'doctor',
        'specialization': 'General Medicine',
        'license_number': 'LIC123456',
        'experience_years': 5,
        'consultation_fee': 500
    }
    
    doctor_response = requests.post(f'{BASE_URL}/signup', json=doctor_data)
    if doctor_response.status_code != 201:
        print(f"FAILED to create doctor: {doctor_response.text}")
        return None, None
    
    doctor_json = doctor_response.json()
    doctor_id = doctor_json.get('user_id')
    if not doctor_id:
        print(f"FAILED: No user_id in response: {doctor_json}")
        return None, None
    print(f"OK - Doctor created (ID: {doctor_id})")
    
    return patient_id, doctor_id

def test_lab_results(patient_id, doctor_id):
    """Test lab results functionality"""
    print("\n=== STEP 2: Testing Lab Results ===")
    
    # Add lab result
    lab_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'test_name': 'Blood Pressure',
        'test_date': datetime.now().strftime('%Y-%m-%d'),
        'result_value': '120/80',
        'result_unit': 'mmHg',
        'reference_range': 'Less than 120/80',
        'status': 'normal',
        'notes': 'Normal blood pressure reading'
    }
    
    response = requests.post(f'{BASE_URL}/add-lab-result', json=lab_data)
    if response.status_code != 201:
        print(f"FAILED to add lab result: {response.text}")
        return False
    
    result = response.json()
    print(f"OK - Lab result added (ID: {result.get('result_id')})")
    
    # Retrieve lab results
    response = requests.get(f'{BASE_URL}/get-lab-results/{patient_id}')
    if response.status_code != 200:
        print(f"FAILED to retrieve lab results: {response.text}")
        return False
    
    results = response.json().get('results', [])
    print(f"OK - Retrieved {len(results)} lab result(s)")
    return True

def test_patient_alerts(patient_id, doctor_id):
    """Test patient alerts functionality"""
    print("\n=== STEP 3: Testing Patient Alerts ===")
    
    # Create alert
    alert_data = {
        'patient_id': patient_id,
        'alert_type': 'high_bp',
        'alert_title': 'High Blood Pressure',
        'alert_message': 'Your recent readings show elevated blood pressure. Please monitor closely and schedule follow-up.',
        'severity': 'high',
        'created_by': doctor_id
    }
    
    response = requests.post(f'{BASE_URL}/add-patient-alert', json=alert_data)
    if response.status_code != 201:
        print(f"FAILED to create alert: {response.text}")
        return False
    
    alert = response.json()
    print(f"OK - Alert created (ID: {alert.get('alert_id')})")
    
    # Get patient alerts
    response = requests.get(f'{BASE_URL}/get-patient-alerts/{patient_id}')
    if response.status_code != 200:
        print(f"FAILED to retrieve alerts: {response.text}")
        return False
    
    alerts = response.json().get('alerts', [])
    print(f"OK - Retrieved {len(alerts)} alert(s)")
    
    # Mark alert as read
    if alerts:
        alert_id = alerts[0]['id']
        response = requests.post(f'{BASE_URL}/mark-alert-read/{alert_id}')
        if response.status_code == 200:
            print(f"OK - Alert marked as read")
    
    return True

def test_follow_ups(patient_id, doctor_id):
    """Test follow-up scheduling"""
    print("\n=== STEP 4: Testing Follow-ups ===")
    
    # Schedule follow-up (7 days from now)
    followup_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    followup_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'follow_up_date': followup_date,
        'follow_up_time': '14:00',
        'reason': 'Blood pressure check-up'
    }
    
    response = requests.post(f'{BASE_URL}/schedule-followup', json=followup_data)
    if response.status_code != 201:
        print(f"FAILED to schedule follow-up: {response.text}")
        return False
    
    followup = response.json()
    print(f"OK - Follow-up scheduled (ID: {followup.get('followup_id')})")
    
    # Get follow-ups
    response = requests.get(f'{BASE_URL}/get-followups/{patient_id}')
    if response.status_code != 200:
        print(f"FAILED to retrieve follow-ups: {response.text}")
        return False
    
    followups = response.json().get('followups', [])
    print(f"OK - Retrieved {len(followups)} follow-up(s)")
    
    return True

def test_appointment_rescheduling(patient_id, doctor_id):
    """Test appointment rescheduling"""
    print("\n=== STEP 5: Testing Appointment Rescheduling ===")
    
    # First, create an appointment
    appt_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    appointment_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'appointment_date': appt_date,
        'appointment_time': '10:00',
        'reason_for_visit': 'Regular check-up'
    }
    
    response = requests.post(f'{BASE_URL}/book-appointment', json=appointment_data)
    if response.status_code != 201:
        print(f"FAILED to create appointment: {response.text}")
        return False
    
    appointment_id = response.json().get('appointment_id')
    print(f"OK - Appointment created (ID: {appointment_id})")
    
    # Reschedule the appointment
    new_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    
    reschedule_data = {
        'appointment_id': appointment_id,
        'new_date': new_date,
        'new_time': '15:00',
        'reason': 'Doctor unavailable on original date'
    }
    
    response = requests.post(f'{BASE_URL}/reschedule-appointment', json=reschedule_data)
    if response.status_code != 200:
        print(f"FAILED to reschedule appointment: {response.text}")
        return False
    
    print(f"OK - Appointment rescheduled to {new_date} at 15:00")
    
    return True

def run_all_tests():
    """Run all enhanced feature tests"""
    print("="*60)
    print("  ENHANCED FEATURES TEST SUITE")
    print("="*60)
    
    try:
        # Create accounts
        patient_id, doctor_id = create_test_accounts()
        if not patient_id or not doctor_id:
            print("❌ Failed to create test accounts")
            return False
        
        # Run feature tests
        tests = [
            ('Lab Results', test_lab_results, [patient_id, doctor_id]),
            ('Patient Alerts', test_patient_alerts, [patient_id, doctor_id]),
            ('Follow-ups', test_follow_ups, [patient_id, doctor_id]),
            ('Appointment Rescheduling', test_appointment_rescheduling, [patient_id, doctor_id]),
        ]
        
        results = []
        for test_name, test_func, args in tests:
            try:
                success = test_func(*args)
                results.append((test_name, success))
            except Exception as e:
                print(f"❌ Error in {test_name}: {str(e)}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "="*60)
        print("  TEST SUMMARY")
        print("="*60)
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "PASSED" if success else "FAILED"
            print(f"{status} - {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print("="*60)
        
        return passed == total
        
    except Exception as e:
        print(f"\nTest suite error: {str(e)}")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
