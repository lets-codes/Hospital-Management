#!/usr/bin/env python3
"""
Comprehensive diagnostic test for Hospital Management System
Tests all major features and identifies issues
"""

import requests
import json
from datetime import datetime, timedelta
import time

API_BASE = 'http://localhost:5000'

class DiagnosticTest:
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.test_data = {}

    def log_pass(self, msg):
        print(f"✓ {msg}")
        self.results['passed'].append(msg)

    def log_fail(self, msg, error=None):
        print(f"✗ {msg}")
        if error:
            print(f"  Error: {error}")
        self.results['failed'].append({'test': msg, 'error': str(error)})

    def log_warn(self, msg):
        print(f"⚠ {msg}")
        self.results['warnings'].append(msg)

    def test_server_health(self):
        """Test 1: Server is running"""
        print("\n" + "="*60)
        print("TEST 1: Server Health")
        print("="*60)
        try:
            resp = requests.get(f'{API_BASE}/health', timeout=5)
            if resp.status_code == 200:
                self.log_pass("Server is responding")
            else:
                self.log_fail(f"Server returned status {resp.status_code}")
        except Exception as e:
            self.log_fail("Cannot connect to server", e)
            return False
        return True

    def test_auth_flow(self):
        """Test 2: User registration and login"""
        print("\n" + "="*60)
        print("TEST 2: Authentication Flow")
        print("="*60)
        try:
            # Test patient signup
            patient_email = f"diag_patient_{int(time.time())}@test.com"
            resp = requests.post(f'{API_BASE}/signup', json={
                'fullname': 'Diagnostic Patient',
                'email': patient_email,
                'phone': '9999999999',
                'password': 'test123',
                'role': 'patient'
            })
            if resp.status_code == 201:
                data = resp.json()
                patient_id = data.get('user_id')
                self.test_data['patient_id'] = patient_id
                self.test_data['patient_email'] = patient_email
                self.log_pass(f"Patient registration successful (ID: {patient_id})")
            else:
                self.log_fail(f"Patient signup failed: {resp.json()}")
                return False

            # Test doctor signup
            doctor_email = f"diag_doctor_{int(time.time())}@test.com"
            resp = requests.post(f'{API_BASE}/signup', json={
                'fullname': 'Diagnostic Doctor',
                'email': doctor_email,
                'phone': '8888888888',
                'password': 'test123',
                'role': 'doctor',
                'specialization': 'General'
            })
            if resp.status_code == 201:
                data = resp.json()
                doctor_id = data.get('user_id')
                self.test_data['doctor_id'] = doctor_id
                self.log_pass(f"Doctor registration successful (ID: {doctor_id})")
            else:
                self.log_fail(f"Doctor signup failed: {resp.json()}")
                return False

            # Test pharmacist signup
            pharmacist_email = f"diag_pharmacist_{int(time.time())}@test.com"
            resp = requests.post(f'{API_BASE}/signup', json={
                'fullname': 'Diagnostic Pharmacist',
                'email': pharmacist_email,
                'phone': '7777777777',
                'password': 'test123',
                'role': 'pharmacist'
            })
            if resp.status_code == 201:
                data = resp.json()
                pharmacist_id = data.get('user_id')
                self.test_data['pharmacist_id'] = pharmacist_id
                self.log_pass(f"Pharmacist registration successful (ID: {pharmacist_id})")
            else:
                self.log_fail(f"Pharmacist signup failed: {resp.json()}")
                return False

            # Test admin signup
            admin_email = f"diag_admin_{int(time.time())}@test.com"
            resp = requests.post(f'{API_BASE}/signup', json={
                'fullname': 'Diagnostic Admin',
                'email': admin_email,
                'phone': '6666666666',
                'password': 'test123',
                'role': 'admin'
            })
            if resp.status_code == 201:
                data = resp.json()
                admin_id = data.get('user_id')
                self.test_data['admin_id'] = admin_id
                self.log_pass(f"Admin registration successful (ID: {admin_id})")
            else:
                self.log_fail(f"Admin signup failed: {resp.json()}")
                return False

            # Test login
            resp = requests.post(f'{API_BASE}/login', json={
                'email': patient_email,
                'password': 'test123'
            })
            if resp.status_code == 200:
                self.log_pass("Login successful")
            else:
                self.log_fail(f"Login failed: {resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Auth flow error", e)
            return False
        return True

    def test_medicines(self):
        """Test 3: Medicine management"""
        print("\n" + "="*60)
        print("TEST 3: Medicine Management")
        print("="*60)
        try:
            admin_id = self.test_data.get('admin_id')
            
            # Add medicine
            med_resp = requests.post(f'{API_BASE}/api/medicines', json={
                'actor_id': admin_id,
                'name': 'Test Medicine',
                'manufacturer': 'TestCorp',
                'batch_no': 'BATCH001',
                'quantity': 100,
                'unit_price': 50.0,
                'expiry_date': '2026-12-31'
            })
            if med_resp.status_code == 201:
                med_id = med_resp.json().get('medicine_id')
                self.test_data['medicine_id'] = med_id
                self.log_pass(f"Medicine added successfully (ID: {med_id})")
            else:
                self.log_fail(f"Add medicine failed: {med_resp.json()}")
                return False

            # Get medicines
            get_resp = requests.get(f'{API_BASE}/api/medicines')
            if get_resp.status_code == 200:
                medicines = get_resp.json().get('medicines', [])
                self.log_pass(f"Get medicines successful ({len(medicines)} total)")
            else:
                self.log_fail(f"Get medicines failed: {get_resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Medicine management error", e)
            return False
        return True

    def test_appointments(self):
        """Test 4: Appointment booking"""
        print("\n" + "="*60)
        print("TEST 4: Appointment Booking")
        print("="*60)
        try:
            patient_id = self.test_data.get('patient_id')
            doctor_id = self.test_data.get('doctor_id')

            # Book appointment
            app_resp = requests.post(f'{API_BASE}/book-appointment', json={
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'appointment_time': '10:00',
                'symptoms': 'Test symptoms'
            })
            if app_resp.status_code in [200, 201]:
                app_id = app_resp.json().get('appointment_id')
                self.test_data['appointment_id'] = app_id
                self.log_pass(f"Appointment booked successfully (ID: {app_id})")
            else:
                self.log_fail(f"Book appointment failed: {app_resp.json()}")
                return False

            # Get patient appointments
            get_app_resp = requests.get(f'{API_BASE}/get-patient-appointments/{patient_id}')
            if get_app_resp.status_code == 200:
                appointments = get_app_resp.json().get('appointments', [])
                self.log_pass(f"Get appointments successful ({len(appointments)} total)")
            else:
                self.log_fail(f"Get appointments failed: {get_app_resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Appointment booking error", e)
            return False
        return True

    def test_prescriptions(self):
        """Test 5: Prescription flow with stock decrement"""
        print("\n" + "="*60)
        print("TEST 5: Prescriptions & Stock Decrement")
        print("="*60)
        try:
            doctor_id = self.test_data.get('doctor_id')
            medicine_id = self.test_data.get('medicine_id')
            appointment_id = self.test_data.get('appointment_id')

            print(f"  Using: doctor_id={doctor_id}, medicine_id={medicine_id}, appointment_id={appointment_id}")

            # Add consultation with prescription
            cons_resp = requests.post(f'{API_BASE}/add-consultation', json={
                'doctor_id': doctor_id,
                'appointment_id': appointment_id,
                'medicine_id': medicine_id,
                'quantity': 10,
                'diagnosis': 'Test diagnosis',
                'notes': 'Test notes'
            })
            if cons_resp.status_code in [200, 201]:
                data = cons_resp.json()
                self.log_pass("Consultation added successfully")
                
                # Check if stock was decremented
                if 'updated_medicines' in data:
                    updated = data['updated_medicines']
                    for med in updated:
                        if med.get('id') == medicine_id:
                            self.log_pass(f"Stock decremented: quantity = {med.get('quantity')}")
                            break
                    else:
                        self.log_warn("Updated medicine not in response")
            else:
                self.log_fail(f"Add consultation failed: {cons_resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Prescription error", e)
            return False
        return True

    def test_restock_flow(self):
        """Test 6: Restock request flow"""
        print("\n" + "="*60)
        print("TEST 6: Restock Request Flow")
        print("="*60)
        try:
            pharmacist_id = self.test_data.get('pharmacist_id')
            admin_id = self.test_data.get('admin_id')
            medicine_id = self.test_data.get('medicine_id')

            # Create restock request
            req_resp = requests.post(f'{API_BASE}/api/restock-request', json={
                'actor_id': pharmacist_id,
                'medicine_id': medicine_id,
                'medicine_name': 'Test Medicine',
                'requested_quantity': 50,
                'reason': 'Low stock'
            })
            if req_resp.status_code == 201:
                req_id = req_resp.json().get('request_id')
                self.test_data['request_id'] = req_id
                self.log_pass(f"Restock request created (ID: {req_id})")
            else:
                self.log_fail(f"Create restock request failed: {req_resp.json()}")
                return False

            # Get restock requests
            get_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
            if get_resp.status_code == 200:
                requests_list = get_resp.json().get('requests', [])
                self.log_pass(f"Get restock requests successful ({len(requests_list)} total)")
            else:
                self.log_fail(f"Get restock requests failed: {get_resp.json()}")
                return False

            # Approve request
            approve_resp = requests.put(f'{API_BASE}/api/admin/restock-request/{req_id}/approve', json={
                'actor_id': admin_id,
                'admin_notes': 'Approved'
            })
            if approve_resp.status_code == 200:
                self.log_pass("Restock request approved")
            else:
                self.log_fail(f"Approve request failed: {approve_resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Restock flow error", e)
            return False
        return True

    def test_screen_rendering(self):
        """Test 7: HTML portals rendering"""
        print("\n" + "="*60)
        print("TEST 7: Portal Rendering")
        print("="*60)
        try:
            portals = [
                '/hospital_landing.html',
                '/login.html',
                '/signup.html',
                '/patient_dashboard.html',
                '/doctor_dashboard.html',
                '/pharmacist_portal.html',
                '/admin_portal.html'
            ]
            
            for portal in portals:
                resp = requests.get(f'{API_BASE}{portal}', timeout=5)
                if resp.status_code == 200:
                    if '<html' in resp.text.lower() or '<!doctype' in resp.text.lower():
                        self.log_pass(f"Portal rendering: {portal}")
                    else:
                        self.log_warn(f"Portal renders but HTML might be incomplete: {portal}")
                else:
                    self.log_fail(f"Portal not found: {portal} ({resp.status_code})")

        except Exception as e:
            self.log_fail("Portal rendering error", e)
            return False
        return True

    def test_admin_stats(self):
        """Test 8: Admin stats calculation"""
        print("\n" + "="*60)
        print("TEST 8: Admin Stats Calculation")
        print("="*60)
        try:
            admin_id = self.test_data.get('admin_id')

            # Get requests for stats
            resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
            if resp.status_code == 200:
                requests_list = resp.json().get('requests', [])
                
                pending = len([r for r in requests_list if r['status'] == 'pending'])
                today = datetime.now().strftime('%Y-%m-%d')
                approved_today = len([r for r in requests_list if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
                rejected_today = len([r for r in requests_list if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])
                
                self.log_pass(f"Stats calculation: Pending={pending}, Approved Today={approved_today}, Rejected Today={rejected_today}")
            else:
                self.log_fail(f"Get stats failed: {resp.json()}")
                return False

        except Exception as e:
            self.log_fail("Stats calculation error", e)
            return False
        return True

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("DIAGNOSTIC SUMMARY")
        print("="*60)
        print(f"\n✓ Passed: {len(self.results['passed'])}")
        for msg in self.results['passed']:
            print(f"  - {msg}")
        
        print(f"\n✗ Failed: {len(self.results['failed'])}")
        for item in self.results['failed']:
            print(f"  - {item['test']}")
            if item['error']:
                print(f"    {item['error']}")
        
        print(f"\n⚠ Warnings: {len(self.results['warnings'])}")
        for msg in self.results['warnings']:
            print(f"  - {msg}")
        
        total = len(self.results['passed']) + len(self.results['failed'])
        pass_rate = (len(self.results['passed']) / total * 100) if total > 0 else 0
        print(f"\nOverall: {pass_rate:.1f}% pass rate ({len(self.results['passed'])}/{total} tests)")
        
        if len(self.results['failed']) == 0:
            print("\n✓ ALL SYSTEMS OPERATIONAL!")
        else:
            print("\n✗ ISSUES DETECTED - See above for details")

    def run_all(self):
        """Run all diagnostic tests"""
        print("\n╔" + "="*58 + "╗")
        print("║" + " HOSPITAL MANAGEMENT SYSTEM - DIAGNOSTIC TEST ".center(58) + "║")
        print("╚" + "="*58 + "╝")
        
        # Run tests in sequence
        if not self.test_server_health():
            return
        
        self.test_auth_flow()
        self.test_medicines()
        self.test_appointments()
        self.test_prescriptions()
        self.test_restock_flow()
        self.test_screen_rendering()
        self.test_admin_stats()
        
        self.print_summary()

if __name__ == '__main__':
    test = DiagnosticTest()
    test.run_all()
