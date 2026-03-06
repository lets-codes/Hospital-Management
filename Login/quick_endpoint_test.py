#!/usr/bin/env python3
"""Quick test of Flask endpoints"""
import requests

print("Testing existing Flask endpoints...")
print()

# Test health endpoint
print("1. Health endpoint (GET)")
response = requests.get('http://localhost:5000/health')
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test get-doctors endpoint
print("2. Get doctors endpoint (GET)")
response = requests.get('http://localhost:5000/get-doctors')
print(f"Status: {response.status_code}")
print()

# Test new add-lab-result endpoint
print("3. Add lab result endpoint (POST)")
data = {
    'patient_id': 1,
    'doctor_id': 1,
    'test_name': 'Test'
}
response = requests.post('http://localhost:5000/add-lab-result', json=data)
print(f"Status: {response.status_code}")
print(f"Response (first 500 chars): {response.text[:500]}")
