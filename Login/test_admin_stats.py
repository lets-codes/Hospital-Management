#!/usr/bin/env python3
"""
Test script to verify admin portal stats (Approved Today, Rejected Today) update correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("TESTING ADMIN APPROVAL/REJECTION STATS UPDATE")
print("=" * 70)

# Step 1: Create admin user
print("\n1. Creating admin user...")
admin_signup = {
    "role": "admin",
    "fullname": "Test Admin",
    "email": f"admin_test_{datetime.now().timestamp()}@test.com",
    "phone": "9876543210",
    "password": "admin123"
}
resp = requests.post(f"{BASE_URL}/signup", json=admin_signup, timeout=5)
print(f"   Admin signup: {resp.status_code}")
admin_data = resp.json()
admin_id = admin_data.get('user_id')
print(f"   Admin ID: {admin_id}")

# Step 2: Create pharmacist user
print("\n2. Creating pharmacist user...")
pharm_signup = {
    "role": "pharmacist",
    "fullname": "Test Pharmacist",
    "email": f"pharm_test_{datetime.now().timestamp()}@test.com",
    "phone": "9876543211",
    "password": "pharm123"
}
resp = requests.post(f"{BASE_URL}/signup", json=pharm_signup, timeout=5)
print(f"   Pharmacist signup: {resp.status_code}")
pharm_data = resp.json()
pharm_id = pharm_data.get('user_id')
print(f"   Pharmacist ID: {pharm_id}")

# Step 3: Login as pharmacist and add a test medicine
print("\n3. Adding a test medicine (as pharmacist)...")
med_payload = {
    "name": "Test Medicine for Stats",
    "manufacturer": "TestCo",
    "batch_no": "BATCH-001",
    "quantity": 50,
    "unit_price": 100.0,
    "sku": "TEST-001",
    "actor_id": pharm_id  # The endpoint uses actor_id not pharmacist_id
}
resp = requests.post(f"{BASE_URL}/api/medicines", json=med_payload, timeout=5)
print(f"   Medicine add: {resp.status_code}")
if resp.status_code != 201:
    print(f"   Response: {resp.text}")
med_data = resp.json()
med_id = med_data.get('medicine_id')
print(f"   Medicine ID: {med_id}")

# Step 4: Create restock requests (pharmacist initiates)
print("\n4. Creating 3 restock requests...")
request_ids = []
for i in range(3):
    req_payload = {
        "medicine_id": med_id,
        "medicine_name": "Test Medicine for Stats",
        "actor_id": pharm_id,  # Use actor_id for permission checks
        "requested_quantity": 10 + i,
        "reason": f"Need stock for test {i}"
    }
    resp = requests.post(f"{BASE_URL}/api/restock-request", json=req_payload, timeout=5)
    print(f"   Request {i+1}: {resp.status_code}")
    if resp.status_code != 201:
        print(f"      Error: {resp.text}")
        continue
    req_data = resp.json()
    req_id = req_data.get('request_id')
    request_ids.append(req_id)
    print(f"      Request ID: {req_id}")

# Step 5: Get initial stats
print("\n5. Getting initial stats (before approvals/rejections)...")
resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}", timeout=5)
print(f"   Get requests: {resp.status_code}")
reqs_data = resp.json()
all_reqs = reqs_data.get('requests', [])
today = datetime.now().strftime('%Y-%m-%d')
pending_before = len([r for r in all_reqs if r['status'] == 'pending'])
approved_before = len([r for r in all_reqs if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
rejected_before = len([r for r in all_reqs if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])
print(f"   Initial stats:")
print(f"      Pending: {pending_before}")
print(f"      Approved Today: {approved_before}")
print(f"      Rejected Today: {rejected_before}")

# Step 6: Approve first request
print("\n6. Admin approves first request...")
resp = requests.put(
    f"{BASE_URL}/api/admin/restock-request/{request_ids[0]}/approve",
    json={"actor_id": admin_id, "admin_notes": "Approved for testing"},
    timeout=5
)
print(f"   Approve: {resp.status_code}")
print(f"   Response: {resp.json()}")

# Step 7: Reject second request
print("\n7. Admin rejects second request...")
resp = requests.put(
    f"{BASE_URL}/api/admin/restock-request/{request_ids[1]}/reject",
    json={"actor_id": admin_id, "rejection_reason": "Out of budget for testing"},
    timeout=5
)
print(f"   Reject: {resp.status_code}")
print(f"   Response: {resp.json()}")

# Step 8: Get updated stats
print("\n8. Getting updated stats (after approvals/rejections)...")
resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}", timeout=5)
print(f"   Get requests: {resp.status_code}")
reqs_data = resp.json()
all_reqs = reqs_data.get('requests', [])
pending_after = len([r for r in all_reqs if r['status'] == 'pending'])
approved_after = len([r for r in all_reqs if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
rejected_after = len([r for r in all_reqs if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])
print(f"   Updated stats:")
print(f"      Pending: {pending_after} (was {pending_before})")
print(f"      Approved Today: {approved_after} (was {approved_before})")
print(f"      Rejected Today: {rejected_after} (was {rejected_before})")

# Step 9: Verify stats changed correctly
print("\n9. Verifying stats changes...")
if pending_after == pending_before - 1:
    print(f"   ✓ Pending decreased by 1 (approval moved it out of pending)")
else:
    print(f"   ✗ Pending should be {pending_before - 1}, but is {pending_after}")

if approved_after == approved_before + 1:
    print(f"   ✓ Approved Today increased by 1 (approval added 1)")
else:
    print(f"   ✗ Approved Today should be {approved_before + 1}, but is {approved_after}")

if rejected_after == rejected_before + 1:
    print(f"   ✓ Rejected Today increased by 1 (rejection added 1)")
else:
    print(f"   ✗ Rejected Today should be {rejected_before + 1}, but is {rejected_after}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
