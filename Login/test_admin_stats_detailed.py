#!/usr/bin/env python3
"""
Full integration test: Create requests, approve/reject, verify stats update in API response
"""
import requests
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"

print("\n" + "="*70)
print("FULL ADMIN STATS INTEGRATION TEST")
print("="*70)

# Setup
print("\n[SETUP] Creating users and medicine...")
admin_resp = requests.post(f"{BASE_URL}/signup", json={
    "role": "admin", "fullname": "AdminTest", "email": f"a{time.time()}@t.com", 
    "phone": "1234567890", "password": "pass123"
}, timeout=5)
admin_id = admin_resp.json()['user_id']

pharm_resp = requests.post(f"{BASE_URL}/signup", json={
    "role": "pharmacist", "fullname": "PharmTest", "email": f"p{time.time()}@t.com",
    "phone": "1234567891", "password": "pass123"
}, timeout=5)
pharm_id = pharm_resp.json()['user_id']

med_resp = requests.post(f"{BASE_URL}/api/medicines", json={
    "actor_id": pharm_id, "name": "TestMed", "quantity": 100, "unit_price": 50,
    "batch_no": "B1", "manufacturer": "M1", "sku": "S1"
}, timeout=5)
med_id = med_resp.json()['medicine_id']

print(f"✓ Admin ID: {admin_id}")
print(f"✓ Pharmacist ID: {pharm_id}")
print(f"✓ Medicine ID: {med_id}")

# Create 2 restock requests
print("\n[STEP 1] Creating 2 restock requests...")
req1_resp = requests.post(f"{BASE_URL}/api/restock-request", json={
    "actor_id": pharm_id, "medicine_id": med_id, "medicine_name": "TestMed",
    "requested_quantity": 10, "reason": "Test 1"
}, timeout=5)
req1_id = req1_resp.json()['request_id']

req2_resp = requests.post(f"{BASE_URL}/api/restock-request", json={
    "actor_id": pharm_id, "medicine_id": med_id, "medicine_name": "TestMed",
    "requested_quantity": 20, "reason": "Test 2"
}, timeout=5)
req2_id = req2_resp.json()['request_id']

print(f"✓ Request 1: {req1_id}")
print(f"✓ Request 2: {req2_id}")

# Get initial stats
print("\n[STEP 2] Get initial stats (before approvals)...")
init_resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}", timeout=5)
init_data = init_resp.json()
all_reqs = init_data.get('requests', [])
today = datetime.now().strftime('%Y-%m-%d')

pending_init = len([r for r in all_reqs if r['status'] == 'pending'])
approved_init = len([r for r in all_reqs if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
rejected_init = len([r for r in all_reqs if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])

print(f"  Pending: {pending_init}")
print(f"  Approved Today: {approved_init}")
print(f"  Rejected Today: {rejected_init}")

# Approve request 1
print("\n[STEP 3] Admin approves request 1...")
approve_resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{req1_id}/approve", json={
    "actor_id": admin_id, "admin_notes": "Approved"
}, timeout=5)
print(f"  Response status: {approve_resp.status_code}")
print(f"  Response: {approve_resp.json()}")

# Get stats after approval
print("\n[STEP 4] Get stats immediately after approval...")
after_approve_resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}", timeout=5)
after_approve_data = after_approve_resp.json()
all_reqs = after_approve_data.get('requests', [])

pending_after_approve = len([r for r in all_reqs if r['status'] == 'pending'])
approved_after_approve = len([r for r in all_reqs if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
rejected_after_approve = len([r for r in all_reqs if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])

print(f"  Pending: {pending_after_approve} (was {pending_init}, change: {pending_after_approve - pending_init})")
print(f"  Approved Today: {approved_after_approve} (was {approved_init}, change: {approved_after_approve - approved_init})")
print(f"  Rejected Today: {rejected_after_approve} (was {rejected_init}, change: {rejected_after_approve - rejected_init})")

# Reject request 2
print("\n[STEP 5] Admin rejects request 2...")
reject_resp = requests.put(f"{BASE_URL}/api/admin/restock-request/{req2_id}/reject", json={
    "actor_id": admin_id, "rejection_reason": "Out of stock"
}, timeout=5)
print(f"  Response status: {reject_resp.status_code}")
print(f"  Response: {reject_resp.json()}")

# Get stats after rejection
print("\n[STEP 6] Get stats after rejection...")
after_reject_resp = requests.get(f"{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}", timeout=5)
after_reject_data = after_reject_resp.json()
all_reqs = after_reject_data.get('requests', [])

pending_after_reject = len([r for r in all_reqs if r['status'] == 'pending'])
approved_after_reject = len([r for r in all_reqs if r['status'] == 'approved' and r.get('approved_at', '').startswith(today)])
rejected_after_reject = len([r for r in all_reqs if r['status'] == 'rejected' and r.get('approved_at', '').startswith(today)])

print(f"  Pending: {pending_after_reject} (was {pending_after_approve})")
print(f"  Approved Today: {approved_after_reject} (was {approved_after_approve})")
print(f"  Rejected Today: {rejected_after_reject} (was {rejected_after_approve})")

# Verify
print("\n[VERIFICATION]")
success = True
if approved_after_approve == approved_init + 1:
    print("✓ Approved count increased by 1 after approval")
else:
    print(f"✗ Approved should be {approved_init + 1}, got {approved_after_approve}")
    success = False

if rejected_after_reject == rejected_after_approve + 1:
    print("✓ Rejected count increased by 1 after rejection")
else:
    print(f"✗ Rejected should be {rejected_after_approve + 1}, got {rejected_after_reject}")
    success = False

if pending_after_reject == 0:
    print("✓ All requests processed (pending = 0)")
else:
    print(f"✗ Pending should be 0, got {pending_after_reject}")
    success = False

print("\n" + "="*70)
if success:
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
else:
    print("✗✗✗ SOME TESTS FAILED ✗✗✗")
print("="*70 + "\n")
