#!/usr/bin/env python3
"""Detailed test of lab-result endpoint"""
import requests
import json

url = 'http://localhost:5000/add-lab-result'
data = {
    'patient_id': 29,
    'doctor_id': 30,
    'test_name': 'Blood Pressure',
    'test_date': '2026-02-17',
    'result_value': '120/80',
    'result_unit': 'mmHg'
}

print("Endpoint URL:", url)
print("Request Data:", json.dumps(data, indent=2))
print()

# Direct Flask test
print("Testing via requests library...")
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Body (first 300 chars):")
print(response.text[:300])
