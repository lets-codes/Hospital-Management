#!/usr/bin/env python3
"""Test pharmacist signup"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("Testing Pharmacist Signup...")
print("=" * 60)

test_data = {
    "fullname": "Test Pharmacist",
    "email": "pharmacist.test@hospital.local",
    "phone": "9876543210",
    "password": "testpass123",
    "role": "pharmacist"
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
        print("\n✓ SUCCESS - Pharmacist signup working!")
    else:
        print(f"\n✗ FAILED - Got status {response.status_code}")
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("\nMake sure server is running on http://localhost:5000")
