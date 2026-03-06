#!/usr/bin/env python3
"""Quick test to verify batch_no field is saved"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000'

# First, create a pharmacist
print("Creating pharmacist...")
pharm_data = {
    'role': 'pharmacist',
    'fullname': 'Test Pharm',
    'email': f'pharm_{int(time.time())}@test.com',
    'phone': '9876543210',
    'password': 'test123'
}
resp = requests.post(f'{BASE_URL}/signup', json=pharm_data)
pharm_id = resp.json().get('user_id')
print(f"Pharmacist ID: {pharm_id}")

# Test: Add medicine with batch number
print("\nAdding medicine with batch number...")
test_data = {
    'name': 'Test Medicine Batch',
    'quantity': 25,
    'unit_price': 20.0,
    'batch_no': 'BATCH-2026-999',
    'expiry_date': '2027-06-30',
    'actor_id': pharm_id
}

response = requests.post(f'{BASE_URL}/api/medicines', json=test_data)
print(f"Add medicine status: {response.status_code}")
result = response.json()
print(f"Result: {json.dumps(result, indent=2)}")

if response.status_code == 201:
    med_id = result.get('medicine_id')
    # Verify by fetching all medicines and finding ours
    resp2 = requests.get(f'{BASE_URL}/api/medicines')
    medicines = resp2.json().get('medicines', [])
    
    # Find the medicine we just added by ID
    found = False
    for m in medicines:
        if m.get('id') == med_id:
            found = True
            print(f"\n✅ Medicine found by ID {med_id}:")
            print(f"   Name: {m.get('name')}")
            print(f"   Batch No: {m.get('batch_no')}")
            print(f"   Expiry Date: {m.get('expiry_date')}")
            print(f"   Quantity: {m.get('quantity')}")
            print(f"   Unit Price: {m.get('unit_price')}")
            break
    
    if not found:
        print(f"\n⚠️ Medicine with ID {med_id} not found in list")
        print(f"Last 3 medicines in database:")
        for m in medicines[-3:]:
            print(f"  - ID: {m.get('id')}, Name: {m.get('name')}, Batch: {m.get('batch_no')}, Expiry: {m.get('expiry_date')}")
else:
    print(f"Error: {result.get('message')}")
