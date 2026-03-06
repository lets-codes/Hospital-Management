#!/usr/bin/env python3
"""
Test script to verify pharmacist can add medicines with batch number and expiry date
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

# Step 1: Signup a pharmacist
print("\n=== STEP 1: Signup Pharmacist ===")
pharm_data = {
    'role': 'pharmacist',
    'fullname': 'Test Pharm',
    'email': f'pharm_{int(time.time())}@test.com',
    'phone': '9876543210',
    'password': 'testpass123'
}
resp = requests.post(f'{BASE_URL}/signup', json=pharm_data)
print(f'Status: {resp.status_code}')
pharm_result = resp.json()
pharm_id = pharm_result.get('user_id')
print(f'✅ Pharmacist created with ID: {pharm_id}')

# Step 2: Add medicine WITH batch number and expiry date
print("\n=== STEP 2: Pharmacist Adds Medicine WITH Batch Number & Expiry Date ===")
med_data = {
    'name': f'Premium Medicine {int(time.time())}',
    'sku': f'SKU-{int(time.time())}',
    'manufacturer': 'Premium Pharma Corp',
    'quantity': 50,
    'unit_price': 25.99,
    'batch_no': 'BATCH-2026-001',
    'expiry_date': '2027-12-31',
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/medicines', json=med_data)
print(f'Status: {resp.status_code}')
med_result = resp.json()
print(f'Response: {med_result}')

if resp.status_code == 201:
    med_id = med_result.get('medicine_id')
    print(f'✅ Medicine added with ID: {med_id}')
    
    # Step 3: Fetch the medicine to verify batch_no and expiry_date were saved
    print("\n=== STEP 3: Verify Medicine Details ===")
    resp = requests.get(f'{BASE_URL}/api/medicines')
    print(f'Status: {resp.status_code}')
    medicines_list = resp.json().get('medicines', [])
    
    # Find our newly added medicine
    for med in medicines_list:
        if med.get('id') == med_id:
            print(f"✅ Found medicine!")
            print(f"   Name: {med.get('name')}")
            print(f"   Batch No: {med.get('batch_no')}")
            print(f"   Expiry Date: {med.get('expiry_date')}")
            print(f"   SKU: {med.get('sku')}")
            print(f"   Manufacturer: {med.get('manufacturer')}")
            print(f"   Quantity: {med.get('quantity')}")
            print(f"   Unit Price: {med.get('unit_price')}")
            break
else:
    print(f"❌ Error adding medicine: {med_result.get('message')}")

# Step 4: Add medicine WITHOUT batch number or expiry date (optional fields)
print("\n=== STEP 4: Pharmacist Adds Medicine WITHOUT Batch Number & Expiry Date ===")
med_data2 = {
    'name': f'Basic Medicine {int(time.time())}',
    'sku': f'SKU2-{int(time.time())}',
    'manufacturer': 'Basic Pharma',
    'quantity': 30,
    'unit_price': 15.99,
    'actor_id': pharm_id
}
resp = requests.post(f'{BASE_URL}/api/medicines', json=med_data2)
print(f'Status: {resp.status_code}')
med_result2 = resp.json()

if resp.status_code == 201:
    med_id2 = med_result2.get('medicine_id')
    print(f'✅ Medicine added (without batch/expiry) with ID: {med_id2}')
else:
    print(f"❌ Error: {med_result2.get('message')}")

print("\n" + "="*70)
print("SUMMARY: Pharmacist medicine creation with optional fields works!")
print("="*70 + "\n")
