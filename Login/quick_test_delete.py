#!/usr/bin/env python3
"""Quick test of delete appointment endpoint"""

import requests

BASE_URL = "http://localhost:5000"

try:
    print("Testing DELETE appointment endpoint...")
    
    # Try to delete a test appointment (ID 999 which doesn't exist)
    response = requests.delete(
        f"{BASE_URL}/delete-appointment/999",
        json={'patient_id': 1},
        timeout=5
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code in [404, 403]:
        print("\n✓ Endpoint is working correctly (expected 404 for non-existent appointment)")
    else:
        print(f"\nResponse indicates endpoint is accessible")
        
except Exception as e:
    print(f"ERROR: {e}")
