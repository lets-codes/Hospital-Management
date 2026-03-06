#!/usr/bin/env python3
"""Test all signup roles"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

roles_to_test = [
    {
        "role": "patient",
        "data": {
            "fullname": "Test Patient",
            "email": f"patient.test.{int(time.time())}@hospital.local",
            "phone": "1111111111",
            "password": "testpass123",
            "role": "patient"
        }
    },
    {
        "role": "doctor", 
        "data": {
            "fullname": "Test Doctor",
            "email": f"doctor.test.{int(time.time())}@hospital.local",
            "phone": "2222222222",
            "password": "testpass123",
            "role": "doctor",
            "specialization": "Cardiology",
            "license_number": "LIC123456",
            "experience_years": 5,
            "consultation_fee": 500
        }
    },
    {
        "role": "pharmacist",
        "data": {
            "fullname": "Test Pharmacist",
            "email": f"pharmacist.test.{int(time.time())}@hospital.local",
            "phone": "3333333333",
            "password": "testpass123",
            "role": "pharmacist"
        }
    },
    {
        "role": "admin",
        "data": {
            "fullname": "Test Admin",
            "email": f"admin.test.{int(time.time())}@hospital.local",
            "phone": "4444444444",
            "password": "testpass123",
            "role": "admin"
        }
    }
]

print("=" * 70)
print("TESTING ALL SIGNUP ROLES")
print("=" * 70)
print()

results = []

for test in roles_to_test:
    role = test["role"]
    data = test["data"]
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json=data,
            timeout=5
        )
        
        success = response.status_code == 201
        status = "✓ PASS" if success else "✗ FAIL"
        
        result = {
            "role": role,
            "status": status,
            "http_status": response.status_code,
            "user_id": response.json().get("user_id") if success else None
        }
        
        results.append(result)
        
        print(f"[{status}] {role.upper():12} - HTTP {response.status_code}")
        if success:
            print(f"       User ID: {response.json().get('user_id')}")
            print(f"       Message: {response.json().get('message')}")
        else:
            print(f"       Error: {response.json().get('message')}")
        
    except Exception as e:
        results.append({
            "role": role,
            "status": "✗ ERROR",
            "error": str(e)
        })
        print(f"[✗ ERROR] {role.upper():12} - {str(e)}")
    
    print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)

for result in results:
    print(f"{result['role'].upper():12} : {result['status']}")

passed = sum(1 for r in results if "PASS" in r["status"])
print()
print(f"Total: {passed}/{len(results)} roles working")

if passed == len(results):
    print("\n✓ ALL SIGNUP ROLES ARE WORKING!")
else:
    print(f"\n✗ Some signups failed")
