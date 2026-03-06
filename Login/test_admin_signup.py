#!/usr/bin/env python3
"""Test admin signup"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("Testing Admin Signup...")
print("=" * 60)

test_data = {
    "fullname": "Test Hospital Admin",
    "email": "admin.test@hospital.local",
    "phone": "9876543211",
    "password": "testadmin123",
    "role": "admin"
}

try:
    response = requests.post(
        f"{BASE_URL}/signup",
        json=test_data,
        timeout=5
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n✓ SUCCESS - Admin signup working!")
    else:
        print(f"\n✗ FAILED - Got status {response.status_code}")
        
except Exception as e:
    print(f"✗ ERROR: {e}")
