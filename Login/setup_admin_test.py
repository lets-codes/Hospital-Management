#!/usr/bin/env python3
"""
Setup test: Create an admin user, log in, set localStorage, then test restock requests
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

# Step 1: Create an admin user for testing
print("\n=== Creating Admin User ===")
admin_email = f'test_admin_{int(time.time())}@test.com'
admin_data = {
    'role': 'admin',
    'fullname': 'Test Admin',
    'email': admin_email,
    'phone': '9876543210',
    'password': 'testpass123'
}
resp = requests.post(f'{BASE_URL}/signup', json=admin_data)
admin_result = resp.json()
admin_id = admin_result.get('user_id')
print(f"✅ Admin created with ID: {admin_id}")
print(f"   Email: {admin_email}")
print(f"   Password: testpass123")

# Step 2: Create a pharmacist user
print("\n=== Creating Pharmacist User ===")
pharm_email = f'test_pharm_{int(time.time())}@test.com'
pharm_data = {
    'role': 'pharmacist',
    'fullname': 'Test Pharmacist',
    'email': pharm_email,
    'phone': '9876543211',
    'password': 'testpass123'
}
resp = requests.post(f'{BASE_URL}/signup', json=pharm_data)
pharm_result = resp.json()
pharm_id = pharm_result.get('user_id')
print(f"✅ Pharmacist created with ID: {pharm_id}")

# Step 3: Pharmacist adds a medicine
print("\n=== Pharmacist Adds Medicine ===")
med_data = {
    'name': f'TESTMED_{int(time.time())}',
    'quantity': 30,
    'unit_price': 25.50,
    'manufacturer': 'Test Corp',
    'expiry_date': '2026-12-31',
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/medicines', json=med_data)
med_result = resp.json()
med_id = med_result.get('medicine_id')
print(f"✅ Medicine added with ID: {med_id}")

# Step 4: Pharmacist creates a restock request
print("\n=== Pharmacist Creates Restock Request ===")
restock_data = {
    'medicine_id': med_id,
    'requested_quantity': 15,
    'reason': 'Running low on stock',
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/restock-request', json=restock_data)
print(f"Status: {resp.status_code}")
if resp.status_code == 201:
    restock_result = resp.json()
    print(f"✅ Restock request created with ID: {restock_result.get('request_id')}")
else:
    print(f"❌ Error: {resp.json()}")

# Step 5: Admin fetches all restock requests
print("\n=== Admin Fetches Restock Requests ===")
resp = requests.get(f'{BASE_URL}/api/admin/restock-requests?actor_id={admin_id}')
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    requests_list = resp.json().get('requests', [])
    print(f"✅ Found {len(requests_list)} restock requests:")
    for req in requests_list[:3]:  # Show first 3
        print(f"   - ID: {req.get('id')}, Medicine: {req.get('medicine_name')}, Status: {req.get('status')}, By: {req.get('pharmacist_name')}")
else:
    print(f"❌ Error: {resp.json()}")

print("\n" + "="*70)
print("NEXT STEP: Open admin portal with this data:")
print(f"1. Go to: http://localhost:5000/admin_portal.html")
print(f"2. You will be redirected to login.html (expected)")
print(f"3. Use email: {admin_email}")
print(f"   Use password: testpass123")
print(f"4. Once logged in, you should see {len(requests_list)} restock request(s)")
print("="*70 + "\n")
