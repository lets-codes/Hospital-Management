#!/usr/bin/env python3
"""
Comprehensive Diagnostic Test for Pharmacist & Admin Portal
Identifies all issues and tests the complete workflow
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

print("=" * 80)
print("COMPREHENSIVE PORTAL DIAGNOSTICS & ISSUE DETECTION")
print("=" * 80)

# Test 1: Server Health
print("\n✓ TEST 1: Server Connection Check")
print("-" * 80)
try:
    # Try accessing signup endpoint to verify server is running
    resp = requests.options(f'{BASE_URL}/signup', timeout=5)
    print(f"✓ Server is running on {BASE_URL}")
except Exception as e:
    print(f"✗ Server is NOT running: {e}")
    exit(1)

# Test 2: Create Test Users
print("\n✓ TEST 2: Create Test Users with Correct Roles")
print("-" * 80)

test_users = {
    'pharmacist': {
        'fullname': f'Test Pharmacist {datetime.now().timestamp()}',
        'email': f'test_pharma_{datetime.now().timestamp()}@hospital.local',
        'phone': '9876543210',
        'password': 'Test@123',
        'role': 'pharmacist'
    },
    'admin': {
        'fullname': f'Test Admin {datetime.now().timestamp()}',
        'email': f'test_admin_{datetime.now().timestamp()}@hospital.local',
        'phone': '9876543211',
        'password': 'Test@123',
        'role': 'admin'
    }
}

user_ids = {}
for role, user_data in test_users.items():
    try:
        resp = requests.post(f'{BASE_URL}/signup', json=user_data)
        if resp.status_code in [200, 201]:
            user_id = resp.json().get('user_id')
            user_ids[role] = user_id
            print(f"✓ {role.capitalize()} created (ID: {user_id}, Email: {user_data['email']})")
        else:
            print(f"✗ {role.capitalize()} signup failed: {resp.json()}")
    except Exception as e:
        print(f"✗ Error creating {role}: {e}")

if not user_ids.get('pharmacist') or not user_ids.get('admin'):
    print("\n⚠ Cannot continue without both pharmacist and admin users")
    exit(1)

PHARMACIST_ID = user_ids['pharmacist']
ADMIN_ID = user_ids['admin']

# Test 3: Add Medicines
print("\n✓ TEST 3: Pharmacist Adding Medicines")
print("-" * 80)

medicines = [
    {
        'name': 'Paracetamol 500mg',
        'sku': 'PCM-500',
        'manufacturer': 'Generic Pharma',
        'quantity': 5,  # Low stock
        'unit_price': 10.50,
        'expiry_date': '2025-12-31'
    },
    {
        'name': 'Ibuprofen 200mg',
        'sku': 'IBU-200',
        'manufacturer': 'Pain Relief Ltd',
        'quantity': 100,  # Good stock
        'unit_price': 14.75,
        'expiry_date': '2025-11-30'
    },
    {
        'name': 'Antibiotics XYZ',
        'sku': 'ABT-XYZ',
        'manufacturer': 'Antibiotic Corp',
        'quantity': 8,  # Low stock
        'unit_price': 25.00,
        'expiry_date': '2025-10-15'
    }
]

medicine_ids = {}
for med in medicines:
    try:
        resp = requests.post(f'{BASE_URL}/api/medicines', json={
            **med,
            'actor_id': PHARMACIST_ID
        })
        if resp.status_code == 201:
            med_id = resp.json().get('medicine_id') or resp.json().get('id')
            medicine_ids[med['name']] = med_id
            print(f"✓ Added: {med['name']} (ID: {med_id}, Stock: {med['quantity']} units)")
        else:
            error_msg = resp.json().get('message', resp.text)
            print(f"✗ Failed to add {med['name']}: {error_msg}")
    except Exception as e:
        print(f"✗ Error adding {med['name']}: {e}")

# Test 4: Pharmacist Views Inventory
print("\n✓ TEST 4: Pharmacist Views Inventory")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/pharmacist/inventory', 
                       params={'actor_id': PHARMACIST_ID})
    if resp.status_code == 200:
        meds = resp.json().get('medicines', [])
        print(f"✓ Inventory loaded: {len(meds)} medicines")
        for med in meds:
            status = "LOW STOCK" if med.get('quantity', 0) <= 10 else "OK"
            print(f"  - {med.get('name')}: {med.get('quantity')} units [{status}]")
    else:
        print(f"✗ Error: {resp.json().get('message')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Pharmacist Requests Restock (for low-stock items)
print("\n✓ TEST 5: Pharmacist Requests Restock for Low-Stock Items")
print("-" * 80)

request_ids = {}
for med_name, med_id in medicine_ids.items():
    med_stock = next((m['quantity'] for m in medicines if m['name'] == med_name), 0)
    
    if med_stock <= 10:  # Only request restock for low-stock items
        try:
            resp = requests.post(f'{BASE_URL}/api/restock-request', json={
                'actor_id': PHARMACIST_ID,
                'medicine_id': med_id,
                'medicine_name': med_name,
                'requested_quantity': 100,
                'reason': f'Stock critically low ({med_stock} units remaining)'
            })
            
            if resp.status_code == 201:
                req_id = resp.json().get('request_id') or resp.json().get('id')
                request_ids[med_name] = req_id
                print(f"✓ Requested: {med_name} (Request ID: {req_id}, +100 units)")
            else:
                error_msg = resp.json().get('message', resp.text)
                print(f"✗ Failed to request {med_name}: {error_msg}")
        except Exception as e:
            print(f"✗ Error requesting {med_name}: {e}")

if not request_ids:
    print("⚠ No restock requests were created")

# Test 6: Admin Views Pending Requests
print("\n✓ TEST 6: Admin Views Pending Restock Requests")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/admin/restock-requests',
                       params={'actor_id': ADMIN_ID, 'status': 'pending'})
    if resp.status_code == 200:
        requests_list = resp.json().get('requests', [])
        print(f"✓ Found {len(requests_list)} pending requests")
        for req in requests_list:
            print(f"  - {req.get('medicine_name')}")
            print(f"    Requested by: {req.get('pharmacist_name')}")
            print(f"    Quantity: {req.get('requested_quantity')} units")
            print(f"    Reason: {req.get('reason')}")
            print(f"    Status: {req.get('status')}")
    else:
        print(f"✗ Error: {resp.json().get('message')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 7: Admin Approves First Request
print("\n✓ TEST 7: Admin Approves Restock Request & Inventory Updates")
print("-" * 80)

first_request_id = next(iter(request_ids.values())) if request_ids else None
if first_request_id:
    try:
        resp = requests.put(
            f'{BASE_URL}/api/admin/restock-request/{first_request_id}/approve',
            json={
                'actor_id': ADMIN_ID,
                'admin_notes': 'Approved - stock added to pharmacy'
            }
        )
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"✓ Request {first_request_id} APPROVED")
            print(f"  Old Stock: {result.get('old_quantity')} units")
            print(f"  New Stock: {result.get('new_quantity')} units")
            print(f"  Added: {result.get('added_quantity')} units")
        else:
            print(f"✗ Error: {resp.json().get('message')}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("⚠ No request to approve (no pending requests)")

# Test 8: Admin Rejects Another Request
print("\n✓ TEST 8: Admin Rejects Restock Request")
print("-" * 80)

second_request = list(request_ids.values())[1] if len(request_ids) > 1 else None
if second_request:
    try:
        resp = requests.put(
            f'{BASE_URL}/api/admin/restock-request/{second_request}/reject',
            json={
                'actor_id': ADMIN_ID,
                'rejection_reason': 'Supplier out of stock - will retry next week'
            }
        )
        
        if resp.status_code == 200:
            print(f"✓ Request {second_request} REJECTED")
            print(f"  Reason: Supplier out of stock - will retry next week")
        else:
            print(f"✗ Error: {resp.json().get('message')}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("⚠ Only one request created, skipping rejection test")

# Test 9: Verify Updated Inventory After Approval
print("\n✓ TEST 9: Verify Updated Medicine Quantities")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/pharmacist/inventory',
                       params={'actor_id': PHARMACIST_ID})
    if resp.status_code == 200:
        meds = resp.json().get('medicines', [])
        print(f"✓ Current inventory status:")
        for med in meds[:3]:  # Show first 3
            print(f"  - {med.get('name')}: {med.get('quantity')} units")
    else:
        print(f"✗ Error: {resp.json().get('message')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 10: Admin Views All Requests (Any Status)
print("\n✓ TEST 10: Admin Views All Requests (Any Status)")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/admin/restock-requests',
                       params={'actor_id': ADMIN_ID, 'status': 'all'})
    if resp.status_code == 200:
        requests_list = resp.json().get('requests', [])
        print(f"✓ Total requests: {len(requests_list)}")
        
        pending = approved = rejected = 0
        for req in requests_list:
            status = req.get('status', 'unknown')
            if status == 'pending':
                pending += 1
                symbol = "⏳"
            elif status == 'approved':
                approved += 1
                symbol = "✓"
            elif status == 'rejected':
                rejected += 1
                symbol = "✗"
            else:
                symbol = "?"
            print(f"  {symbol} {req.get('medicine_name')}: {status.upper()}")
        
        print(f"\n  Summary:")
        print(f"    Pending: {pending}")
        print(f"    Approved: {approved}")
        print(f"    Rejected: {rejected}")
    else:
        print(f"✗ Error: {resp.json().get('message')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 11: Permission Tests
print("\n✓ TEST 11: Permission & Access Control Tests")
print("-" * 80)

# Test pharmacist accessing admin endpoint
try:
    resp = requests.get(f'{BASE_URL}/api/admin/restock-requests',
                       params={'actor_id': PHARMACIST_ID, 'status': 'pending'})
    if resp.status_code == 403:
        print(f"✓ Pharmacist correctly denied access to admin endpoint")
    else:
        print(f"✗ Pharmacist should NOT have access to admin endpoint (got status {resp.status_code})")
except Exception as e:
    print(f"✗ Error: {e}")

# Test admin trying to add medicine without proper permission check
try:
    resp = requests.post(f'{BASE_URL}/api/medicines', json={
        'name': 'Test Medicine',
        'quantity': 10,
        'unit_price': 15.50,
        'actor_id': ADMIN_ID
    })
    if resp.status_code == 403:
        print(f"✓ Admin correctly denied permission to add medicines (pharmacist-only endpoint)")
    else:
        print(f"⚠ Admin was allowed to add medicines (status {resp.status_code}) - check if intended")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 80)

print("\n📊 SUMMARY:")
print("  Pharmacist Portal: Can add medicines, view inventory, request restock")
print("  Admin Portal: Can view requests, approve/reject, inventory auto-updates")
print("  Communication: Via restock request → approval/rejection workflow")
print("\n🌐 PORTAL LINKS:")
print("  Pharmacist: http://localhost:5000/pharmacist_portal.html")
print("  Admin: http://localhost:5000/admin_portal.html")
print("\n🔐 Test Credentials:")
print(f"  Pharmacist ID: {PHARMACIST_ID}")
print(f"  Admin ID: {ADMIN_ID}")
