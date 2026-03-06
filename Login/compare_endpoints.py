#!/usr/bin/env python3
"""Test working vs non-working endpoints"""

import requests
import json

BASE_URL = 'http://localhost:5000'

# Test existing working endpoint
print("=" * 60)
print("Testing /signup endpoint (KNOWN WORKING)")
print("=" * 60)

try:
    options_response = requests.options(
        f'{BASE_URL}/signup',
        timeout=5
    )
    print(f"OPTIONS Status: {options_response.status_code}")
    print(f"Allow Header: {options_response.headers.get('Allow', 'NOT SET')}")
    print(f"Access-Control-Allow-Methods: {options_response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    
except Exception as e:
    print(f"ERROR: {e}")

# Compare with new endpoint
print("\n" + "=" * 60)
print("Testing /add-lab-result endpoint (NOT WORKING)")
print("=" * 60)

try:
    options_response = requests.options(
        f'{BASE_URL}/add-lab-result',
        timeout=5
    )
    print(f"OPTIONS Status: {options_response.status_code}")
    print(f"Allow Header: {options_response.headers.get('Allow', 'NOT SET')}")
    print(f"Access-Control-Allow-Methods: {options_response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
