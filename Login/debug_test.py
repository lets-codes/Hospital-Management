#!/usr/bin/env python3
"""Debug script to test POST endpoint directly"""

import requests
import json

BASE_URL = 'http://localhost:5000'

# Test data
test_data = {
    "patient_id": 39,
    "doctor_id": 40,
    "test_name": "Blood Test",
    "result_value": "120",
    "result_unit": "mg/dL",
    "reference_range": "70-100",
    "status": "normal",
    "notes": "Debug test"
}

print("=" * 60)
print("Testing /add-lab-result endpoint")
print("=" * 60)
print(f"\nRequest URL: {BASE_URL}/add-lab-result")
print(f"Method: POST")
print(f"Headers: Content-Type: application/json")
print(f"Body: {json.dumps(test_data, indent=2)}")

try:
    # First test OPTIONS (preflight)
    print("\n\n1. Testing OPTIONS (CORS preflight)...")
    options_response = requests.options(
        f'{BASE_URL}/add-lab-result',
        headers={'Origin': 'http://localhost:3000'},
        timeout=5
    )
    print(f"Status: {options_response.status_code}")
    print(f"Allow Header: {options_response.headers.get('Allow', 'NOT SET')}")
    print(f"Access-Control-Allow-Methods: {options_response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    print(f"All Response Headers: {dict(options_response.headers)}")
    
    # Now test actual POST
    print("\n\n2. Testing POST request...")
    response = requests.post(
        f'{BASE_URL}/add-lab-result',
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Content:")
    print(response.text)
    print(f"\nJSON Response: {response.json()}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
