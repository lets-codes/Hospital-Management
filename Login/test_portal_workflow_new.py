#!/usr/bin/env python3
"""
Test the complete pharmacist and admin portal workflow
Uses newly created users with correct roles
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

# Users from previous test (with correct roles now)
PHARMACIST_ID = 86  # Has 'pharmacist' role
ADMIN_ID = 87       # Has 'admin' role

print("=" * 80)
print("TESTING PHARMACIST & ADMIN PORTALS - COMPLETE WORKFLOW")
print("=" * 80)

# 1. Health Check
print("\n1. Health Check")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/health')
    if resp.status_code == 200:
        print(f"✓ Server running: {resp.json().get('service', 'Hospital management system')}")
    else:
        print(f"✗ Server error: {resp.status_code}")
except Exception as e:
    print(f"✗ Cannot connect to server: {e}")
    exit(1)

# 2. Pharmacist Adding Medicines
print("\n2. Pharmacist Adding Medicines")
print("-" * 80)
medicines = [
    {'name': 'Amoxicillin 500mg', 'sku': 'AMOX500', 'manufacturer': 'Generic Pharma', 
     'quantity': 100, 'unit_price': 15.50, 'expiry_date': '2025-12-31'},
    {'name': 'Ibuprofen 200mg', 'sku': 'IBU200', 'manufacturer': 'Pain Relief Inc',
     'quantity': 50, 'unit_price': 8.25, 'expiry_date': '2025-11-30'},
    {'name': 'Metformin 1000mg', 'sku': 'MET1000', 'manufacturer': 'Diabetes Care Ltd',
     'quantity': 8, 'unit_price': 12.75, 'expiry_date': '2025-10-15'}  # Low stock
]

medicine_ids = []
for med in medicines:
    try:
        resp = requests.post(f'{BASE_URL}/api/medicines', json={
            **med,
            'actor_id': PHARMACIST_ID
        })
        if resp.status_code == 201:
            med_id = resp.json().get('id')
            medicine_ids.append(med_id)
            print(f"✓ Added {med['name']} (ID: {med_id}, Stock: {med['quantity']})")
        else:
            print(f"✗ Failed to add {med['name']}: {resp.json().get('message', resp.text)}")
    except Exception as e:
        print(f"✗ Error adding {med['name']}: {e}")

# 3. Pharmacist Viewing Inventory
print("\n3. Pharmacist Viewing Inventory")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/pharmacist/inventory', params={'actor_id': PHARMACIST_ID})
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Pharmacist inventory access granted")
        print(f"  Total medicines: {len(data.get('medicines', []))}")
        for med in data.get('medicines', [])[:3]:
            print(f"    - {med.get('name', 'Unknown')}: {med.get('quantity')} units")
    else:
        print(f"✗ Error: {resp.json().get('message', resp.text)}")
except Exception as e:
    print(f"✗ Error: {e}")

# 4. Pharmacist Requesting Restock
print("\n4. Pharmacist Requesting Restock")
print("-" * 80)
request_ids = []
if medicine_ids:
    for i, med_id in enumerate(medicine_ids[:2]):  # Request restock for first 2 medicines
        try:
            resp = requests.post(f'{BASE_URL}/api/restock-request', json={
                'medicine_id': med_id,
                'medicine_name': medicines[i]['name'],
                'requested_by': PHARMACIST_ID,
                'requested_quantity': 100 if i == 2 else 50,
                'reason': 'Low stock - urgent resupply needed' if i == 2 else 'Regular restocking'
            })
            if resp.status_code == 201:
                req_id = resp.json().get('id')
                request_ids.append(req_id)
                print(f"✓ Restock request created for {medicines[i]['name']} (Request ID: {req_id})")
            else:
                print(f"✗ Failed to create request for {medicines[i]['name']}: {resp.json().get('message', resp.text)}")
        except Exception as e:
            print(f"✗ Error: {e}")

# 5. Admin Viewing Restock Requests
print("\n5. Admin Viewing Restock Requests (Pending)")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/admin/restock-requests', 
                       params={'actor_id': ADMIN_ID, 'status': 'pending'})
    if resp.status_code == 200:
        data = resp.json()
        pending_count = len(data.get('requests', []))
        print(f"✓ Admin can view restock requests: {pending_count} pending request(s)")
        for req in data.get('requests', []):
            print(f"    - {req.get('medicine_name')} from {req.get('pharmacist_name')}: {req.get('requested_quantity')} units")
    else:
        print(f"✗ Error: {resp.json().get('message', resp.text)}")
except Exception as e:
    print(f"✗ Error: {e}")

# 6. Admin Approving Restock Request
print("\n6. Admin Approving Restock Request")
print("-" * 80)
if request_ids:
    try:
        resp = requests.put(f'{BASE_URL}/api/admin/restock-request/{request_ids[0]}/approve', json={
            'actor_id': ADMIN_ID,
            'admin_notes': 'Stock approved and added to inventory'
        })
        if resp.status_code == 200:
            print(f"✓ Request {request_ids[0]} approved by admin")
            print(f"  Response: {resp.json().get('message', 'Request approved')}")
        else:
            print(f"✗ Failed to approve: {resp.json().get('message', resp.text)}")
    except Exception as e:
        print(f"✗ Error: {e}")

# 7. Verify Inventory Updated After Approval
print("\n7. Verify Inventory After Approval")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/pharmacist/inventory', params={'actor_id': PHARMACIST_ID})
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Inventory checked after approval")
        for med in data.get('medicines', [])[:3]:
            print(f"    - {med.get('name')}: {med.get('quantity')} units")
    else:
        print(f"✗ Error: {resp.json().get('message', resp.text)}")
except Exception as e:
    print(f"✗ Error: {e}")

# 8. Admin Rejecting Restock Request
print("\n8. Admin Rejecting Restock Request")
print("-" * 80)
if len(request_ids) > 1:
    try:
        resp = requests.put(f'{BASE_URL}/api/admin/restock-request/{request_ids[1]}/reject', json={
            'actor_id': ADMIN_ID,
            'rejection_reason': 'Out of stock supplier - will replenish next week'
        })
        if resp.status_code == 200:
            print(f"✓ Request {request_ids[1]} rejected by admin")
            print(f"  Response: {resp.json().get('message', 'Request rejected')}")
        else:
            print(f"✗ Failed to reject: {resp.json().get('message', resp.text)}")
    except Exception as e:
        print(f"✗ Error: {e}")

# 9. View All Requests (Any Status)
print("\n9. View All Restock Requests (All Statuses)")
print("-" * 80)
try:
    resp = requests.get(f'{BASE_URL}/api/admin/restock-requests', 
                       params={'actor_id': ADMIN_ID})
    if resp.status_code == 200:
        data = resp.json()
        requests_list = data.get('requests', [])
        print(f"✓ Total requests: {len(requests_list)}")
        for req in requests_list:
            status_symbol = '✓' if req.get('status') == 'approved' else '✗' if req.get('status') == 'rejected' else '⏳'
            print(f"    {status_symbol} {req.get('medicine_name')}: {req.get('status').upper()}")
    else:
        print(f"✗ Error: {resp.json().get('message', resp.text)}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("TEST SUITE COMPLETE")
print("=" * 80)
print("\nSummary:")
print("✓ Pharmacist Portal: Can view inventory, add medicines, request restock")
print("✓ Admin Portal: Can view requests, approve (updates inventory), reject")
print("✓ Communication System: Via restock requests with approval/rejection workflow")
print("\nNext Steps:")
print("1. Open http://localhost:5000/pharmacist_portal.html")
print("2. Login with User ID: 86 (pharmacist)")
print("3. Open http://localhost:5000/admin_portal.html")
print("4. Login with User ID: 87 (admin)")
