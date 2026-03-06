#!/usr/bin/env python3
"""Test OPTIONS request"""
import requests

url = 'http://localhost:5000/add-lab-result'

print("1. Testing OPTIONS request...")
response = requests.options(url)
print(f"Status: {response.status_code}")
print(f"Allow header: {response.headers.get('Allow')}")
print()

print("2. Testing POST request...")
data = {
    'patient_id': 1,
    'doctor_id': 1,
    'test_name': 'Test'
}
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Allow header: {response.headers.get('Allow')}")
print()

print("3. List all Flask routes...")
from server_patient_doctor import app
matching_routes = [r for r in app.url_map.iter_rules() if 'add-lab' in str(r.rule)]
for route in matching_routes:
    print(f"Route: {route.rule}")
    print(f"Methods: {list(route.methods)}")
