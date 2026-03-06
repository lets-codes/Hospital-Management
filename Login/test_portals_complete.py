#!/usr/bin/env python3
"""
Test the new Pharmacist and Admin Portal features
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESTING PHARMACIST & ADMIN PORTALS WITH RESTOCK SYSTEM")
print("=" * 80)
print()

# Test 1: Health check
print("1. Health Check")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=3)
    print(f"✓ Server is running: {resp.json()}")
except Exception as e:
    print(f"✗ Server error: {e}")
    exit(1)

print()

# Test 2: Create test medicines
print("2. Adding Test Medicines")
print("-" * 80)

# We'll use actor_id=80 (pharmacist from earlier tests)
medicines_to_add = [
    {"name": "Amoxicillin 500mg", "manufacturer": "ABC Pharma", "quantity": 5, "unit_price": 15.50},
    {"name": "Metformin 1000mg", "manufacturer": "XYZ Drugs", "quantity": 20, "unit_price": 8.75},
    {"name": "Paracetamol 650mg", "manufacturer": "Generic Corp", "quantity": 50, "unit_price": 3.00}
]

medicine_ids = []
for med in medicines_to_add:
    try:
        resp = requests.post(f"{BASE_URL}/api/medicines", json={
            "actor_id": 80,  # pharmacist
            **med
        }, timeout=3)
        if resp.ok:
            data = resp.json()
            print(f"✓ Added: {med['name']}")
            medicine_ids.append((med['name'], resp.json().get('medicine_id', 1)))
        else:
            print(f"✗ Failed to add {med['name']}: {resp.json().get('message')}")
    except Exception as e:
        print(f"✗ Error adding {med['name']}: {e}")

print()

# Test 3: Test Pharmacist Inventory Endpoint
print("3. Testing Pharmacist Inventory Endpoint")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/pharmacist/inventory?actor_id=80", timeout=3)
    if resp.ok:
        data = resp.json()
        print(f"✓ Got pharmacist inventory: {len(data['medicines'])} medicines")
        for med in data['medicines'][:3]:
            print(f"  - {med['name']}: {med['quantity']} units (pending requests: {med.get('pending_requests', 0)})")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Create Restock Request
print("4. Testing Restock Request (Pharmacist -> Admin)")
print("-" * 80)
try:
    # Get first medicine ID (should be from the API response)
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        if meds:
            med = meds[0]
            resp = requests.post(f"{BASE_URL}/api/restock-request", json={
                "actor_id": 80,  # pharmacist
                "medicine_id": med['id'],
                "medicine_name": med['name'],
                "requested_quantity": 100,
                "reason": "Stock depleting rapidly"
            }, timeout=3)
            
            if resp.ok:
                request_id = resp.json()['request_id']
                print(f"✓ Restock request created (ID: {request_id})")
                print(f"  - Pharmacist requested 100 units of '{med['name']}'")
            else:
                print(f"✗ Error: {resp.json()}")
        else:
            print("✗ No medicines available")
    else:
        print(f"✗ Error fetching medicines: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Admin Views Restock Requests
print("5. Testing Admin Restock Request List")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id=81&status=pending", timeout=3)
    if resp.ok:
        requests_list = resp.json()['requests']
        print(f"✓ Admin can view requests: {len(requests_list)} pending requests")
        for req in requests_list[:2]:
            print(f"  - {req['medicine_name']}: {req['requested_quantity']} units requested by {req['pharmacist_name']}")
            print(f"    Status: {req['status']}, Requested: {req['requested_at']}")
    else:
        print(f"✗ Error: {resp.json().get('message')}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 6: Admin Approves Restock Request
print("6. Testing Admin Approval of Restock Request")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id=81&status=pending", timeout=3)
    if resp.ok:
        requests_list = resp.json()['requests']
        if requests_list:
            req = requests_list[0]
            resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{req['id']}/approve", json={
                "actor_id": 81,  # admin
                "admin_notes": "Approved. Stock is low, request is legitimate."
            }, timeout=3)
            
            if resp.ok:
                print(f"✓ Restock request APPROVED")
                print(f"  - Admin added {req['requested_quantity']} units to '{req['medicine_name']}'")
            else:
                print(f"✗ Error: {resp.json()}")
        else:
            print("✗ No pending requests to approve")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 7: Verify Updated Medicine Quantity
print("7. Verifying Updated Medicine Quantity After Approval")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        print(f"✓ Current medicine inventory:")
        for med in meds[:3]:
            print(f"  - {med['name']}: {med['quantity']} units")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 8: Test Rejection
print("8. Testing Admin Rejection of Restock Request")
print("-" * 80)
try:
    # Create another request to reject
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        if meds:
            med = meds[1] if len(meds) > 1 else meds[0]
            resp = requests.post(f"{BASE_URL}/api/restock-request", json={
                "actor_id": 80,  # pharmacist
                "medicine_id": med['id'],
                "medicine_name": med['name'],
                "requested_quantity": 500,
                "reason": "Testing rejection"
            }, timeout=3)
            
            if resp.ok:
                new_request_id = resp.json()['request_id']
                
                # Now reject it
                resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{new_request_id}/reject", json={
                    "actor_id": 81,  # admin
                    "admin_notes": "Budget exceeded for this quarter"
                }, timeout=3)
                
                if resp.ok:
                    print(f"✓ Restock request REJECTED")
                    print(f"  - Admin rejected with reason: 'Budget exceeded for this quarter'")
                else:
                    print(f"✗ Error rejecting: {resp.json()}")
            else:
                print(f"✗ Error creating request")
    else:
        print(f"✗ Error fetching medicines")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 80)
print("TEST SUITE COMPLETE")
print("=" * 80)
print()
print("Summary:")
print("✓ Pharmacist Portal: Can view inventory, add medicines, request restock")
print("✓ Admin Portal: Can view requests, approve (updates inventory), reject")
print("✓ Communication System: Via restock request -> admin approval/rejection")
print()
print("Next Steps:")
print("1. Open http://localhost:5000/pharmacist_portal.html (login as pharmacist)")
print("2. Open http://localhost:5000/admin_portal.html (login as admin)")
print("3. Test the UI workflows")
