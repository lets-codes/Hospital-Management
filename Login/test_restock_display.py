#!/usr/bin/env python3
"""
Test script to verify restock requests are displaying in admin portal
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

# Step 1: Signup a pharmacist
print("\n=== STEP 1: Signup Pharmacist ===")
pharm_data = {
    'role': 'pharmacist',
    'fullname': 'Pharm Test',
    'email': f'pharm_test_{int(time.time())}@test.com',
    'phone': '9999999999',
    'password': 'password123'
}
resp = requests.post(f'{BASE_URL}/signup', json=pharm_data)
print(f'SIGNUP STATUS: {resp.status_code}')
pharm_user = resp.json()
print(f'Pharmacist: {pharm_user}')
pharm_id = pharm_user.get('user_id')

# Step 2: Signup an admin
print("\n=== STEP 2: Signup Admin ===")
admin_data = {
    'role': 'admin',
    'fullname': 'Admin Test',
    'email': f'admin_test_{int(time.time())}@test.com',
    'phone': '8888888888',
    'password': 'password123'
}
resp = requests.post(f'{BASE_URL}/signup', json=admin_data)
print(f'SIGNUP STATUS: {resp.status_code}')
admin_user = resp.json()
print(f'Admin: {admin_user}')
admin_id = admin_user.get('user_id')

# Step 3: Pharmacist adds a medicine
print("\n=== STEP 3: Pharmacist Adds Medicine ===")
med_data = {
    'name': f'Test Medicine {int(time.time())}',
    'quantity': 50,
    'unit_price': 15.99,
    'manufacturer': 'Test Mfg',
    'expiry_date': '2026-12-31',
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/medicines', json=med_data)
print(f'ADD MEDICINE STATUS: {resp.status_code}')
med_result = resp.json()
print(f'Medicine result: {med_result}')
med_id = med_result.get('medicine_id')

# Step 4: Pharmacist requests restock
print("\n=== STEP 4: Pharmacist Requests Restock ===")
restock_data = {
    'medicine_id': med_id,
    'requested_quantity': 20,
    'reason': 'Low inventory',
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/restock-request', json=restock_data)
print(f'RESTOCK REQUEST STATUS: {resp.status_code}')
restock_result = resp.json()
print(f'Restock result: {restock_result}')

# Step 5: Admin fetches all restock requests
print("\n=== STEP 5: Admin Fetches Restock Requests ===")
resp = requests.get(f'{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}')
print(f'FETCH RESTOCK STATUS: {resp.status_code}')
restock_list = resp.json()
print(f'Restock requests count: {len(restock_list.get("requests", []))}')
if restock_list.get('requests'):
    for req in restock_list['requests']:
        print(f"  - Request ID: {req.get('id')}, Medicine: {req.get('medicine_name')}, Status: {req.get('status')}")
else:
    print(f"ERROR: {restock_list.get('message')}")

print("\n✅ Test complete!")
