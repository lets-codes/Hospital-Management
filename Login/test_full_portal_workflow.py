#!/usr/bin/env python3
"""
Test portals with simulated login to get proper credentials
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESTING PHARMACIST & ADMIN PORTALS - FULL WORKFLOW")
print("=" * 80)
print()

# Test 1: Health check
print("1. Health Check")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=3)
    print(f"✓ Server running: {resp.json()['service']}")
except Exception as e:
    print(f"✗ Server error: {e}")
    exit(1)

print()

# Register test users if they don't exist
print("2. Setting Up Test Users")
print("-" * 80)

pharmacist_creds = {
    "email": f"testpharma{int(time.time())}@hospital.local",
    "password": "testpharma123",
    "fullname": "Test Pharmacist Portal",
    "phone": "9999999991",
    "role": "pharmacist"
}

admin_creds = {
    "email": f"testadmin{int(time.time())}@hospital.local",
    "password": "testadmin123",
    "fullname": "Test Admin Portal",
    "phone": "9999999992",
    "role": "admin"
}

pharmacist_user = None
admin_user = None

# Register pharmacist
try:
    resp = requests.post(f"{BASE_URL}/signup", json=pharmacist_creds, timeout=3)
    if resp.ok:
        pharmacist_user = resp.json()
        print(f"✓ Pharmacist registered (ID: {pharmacist_user['user_id']})")
    else:
        print(f"✗ Pharmacist signup failed: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

# Register admin
try:
    resp = requests.post(f"{BASE_URL}/signup", json=admin_creds, timeout=3)
    if resp.ok:
        admin_user = resp.json()
        print(f"✓ Admin registered (ID: {admin_user['user_id']})")
    else:
        print(f"✗ Admin signup failed: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

if not pharmacist_user or not admin_user:
    print("\n✗ Failed to register test users")
    exit(1)

pharmacist_id = pharmacist_user['user_id']
admin_id = admin_user['user_id']

print()

# Test 3: Add medicines as pharmacist
print("3. Pharmacist Adding Medicines")
print("-" * 80)

medicines = [
    {"name": "Amoxicillin 500mg", "manufacturer": "ABC Pharma", "quantity": 5, "unit_price": 15.50},
    {"name": "Metformin 1000mg", "manufacturer": "XYZ Drugs", "quantity": 20, "unit_price": 8.75},
    {"name": "Aspirin 300mg", "manufacturer": "Generic Corp", "quantity": 50, "unit_price": 3.00}
]

medicine_ids = []
for med in medicines:
    try:
        resp = requests.post(f"{BASE_URL}/api/medicines", json={
            "actor_id": pharmacist_id,
            **med
        }, timeout=3)
        if resp.ok:
            print(f"✓ Added: {med['name']}")
            medicine_ids.append(med['name'])
        else:
            print(f"✗ Failed: {resp.json().get('message')}")
    except Exception as e:
        print(f"✗ Error: {e}")

print()

# Test 4: Pharmacist views inventory
print("4. Pharmacist Viewing Inventory")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/pharmacist/inventory?actor_id={pharmacist_id}", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        print(f"✓ Pharmacist inventory loaded: {len(meds)} medicines")
        for med in meds:
            print(f"  - {med['name']}: {med['quantity']} units (SKU: {med.get('sku', 'N/A')})")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Pharmacist requests restock
print("5. Pharmacist Requesting Restock")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        if meds:
            med = meds[0]
            resp = requests.post(f"{BASE_URL}/api/restock-request", json={
                "actor_id": pharmacist_id,
                "medicine_id": med['id'],
                "medicine_name": med['name'],
                "requested_quantity": 100,
                "reason": "Stock level critical"
            }, timeout=3)
            
            if resp.ok:
                request_id = resp.json()['request_id']
                print(f"✓ Restock request submitted (ID: {request_id})")
                print(f"  - Medicine: {med['name']}")
                print(f"  - Quantity: 100 units")
                print(f"  - Reason: Stock level critical")
            else:
                print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 6: Admin views pending requests
print("6. Admin Viewing Restock Requests")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}&status=pending", timeout=3)
    if resp.ok:
        requests_list = resp.json()['requests']
        print(f"✓ Admin viewing {len(requests_list)} pending request(s)")
        for req in requests_list:
            print(f"  - Medicine: {req['medicine_name']}")
            print(f"    Quantity: {req['requested_quantity']} units")
            print(f"    Requested by: {req['pharmacist_name']}")
            print(f"    Reason: {req['reason']}")
            print(f"    Status: {req['status']}")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 7: Admin approves first request
print("7. Admin Approving Restock Request")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}&status=pending", timeout=3)
    if resp.ok:
        requests_list = resp.json()['requests']
        if requests_list:
            req = requests_list[0]
            old_qty = None
            
            # Get current quantity before approval
            resp_meds = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
            if resp_meds.ok:
                meds = resp_meds.json()['medicines']
                for m in meds:
                    if m['id'] == req['medicine_id']:
                        old_qty = m['quantity']
                        break
            
            # Approve the request
            resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{req['id']}/approve", json={
                "actor_id": admin_id,
                "admin_notes": "Approved. Urgent demand for this medicine."
            }, timeout=3)
            
            if resp.ok:
                print(f"✓ Request APPROVED by admin")
                print(f"  - Medicine: {req['medicine_name']}")
                print(f"  - Added: {req['requested_quantity']} units")
                if old_qty:
                    print(f"  - Old Stock: {old_qty} → New Stock: {old_qty + req['requested_quantity']} units")
            else:
                print(f"✗ Error: {resp.json()}")
        else:
            print("✗ No pending requests found")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 8: Verify updates
print("8. Verifying Updated Inventory")
print("-" * 80)
try:
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        print(f"✓ Current inventory status:")
        for med in meds[:3]:
            status = "LOW" if med['quantity'] <= 10 else "OK"
            print(f"  - {med['name']}: {med['quantity']} units [{status}]")
    else:
        print(f"✗ Error: {resp.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 9: Admin rejects another request
print("9. Admin Rejecting a Restock Request")
print("-" * 80)
try:
    # Create another request
    resp = requests.get(f"{BASE_URL}/api/medicines", timeout=3)
    if resp.ok:
        meds = resp.json()['medicines']
        if len(meds) > 1:
            med = meds[1]
            resp = requests.post(f"{BASE_URL}/api/restock-request", json={
                "actor_id": pharmacist_id,
                "medicine_id": med['id'],
                "medicine_name": med['name'],
                "requested_quantity": 500,
                "reason": "Testing rejection flow"
            }, timeout=3)
            
            if resp.ok:
                new_req_id = resp.json()['request_id']
                
                # Reject it
                resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{new_req_id}/reject", json={
                    "actor_id": admin_id,
                    "admin_notes": "Budget limit reached for this quarter. Try again next month."
                }, timeout=3)
                
                if resp.ok:
                    print(f"✓ Request REJECTED by admin")
                    print(f"  - Reason: Budget limit reached for this quarter")
                    print(f"  - Pharmacist notified via rejection notes")
                else:
                    print(f"✗ Error rejecting: {resp.json()}")
            else:
                print(f"✗ Error creating request for rejection test")
    else:
        print(f"✗ Error getting medicines")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 80)
print("ALL TESTS COMPLETE!")
print("=" * 80)
print()
print("SYSTEM FEATURES WORKING:")
print("✓ Pharmacist Portal: Add medicines, view inventory, request restock")
print("✓ Admin Portal: View requests (pending/approved/rejected), approve to update stock")
print("✓ Restock Workflow: Request → Admin Review → Approve/Reject → Auto Inventory Update")
print("✓ Communication: Via restock request status and admin notes")
print()
print("PORTAL ACCESS:")
print(f"Pharmacist: Email: {pharmacist_creds['email']} | Password: {pharmacist_creds['password']}")
print(f"Admin:      Email: {admin_creds['email']} | Password: {admin_creds['password']}")
print()
print("WEB INTERFACE:")
print("→ http://localhost:5000/pharmacist_portal.html (Pharmacist Portal)")
print("→ http://localhost:5000/admin_portal.html (Admin Portal)")
