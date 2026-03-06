#!/usr/bin/env python3
"""
Test Pharmacist Request Viewing Feature
Verifies that pharmacist can see their submitted requests with status
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

print("=" * 80)
print("TEST: Pharmacist Viewing Their Own Restock Requests")
print("=" * 80)

# Use the previous test users
PHARMACIST_ID = 91  # From previous test
ADMIN_ID = 92  # From previous test

print("\n1. Pharmacist Views Their Submitted Requests")
print("-" * 80)

try:
    resp = requests.get(f'{BASE_URL}/api/pharmacist/restock-requests',
                       params={'actor_id': PHARMACIST_ID})
    
    if resp.status_code == 200:
        requests_data = resp.json().get('requests', [])
        print(f"✓ Pharmacist retrieved {len(requests_data)} submitted requests\n")
        
        print("Request Details:")
        print("-" * 80)
        
        for req in requests_data:
            print(f"\nMedicine: {req.get('medicine_name')}")
            print(f"  Status: {req.get('status').upper()}")
            print(f"  Requested Quantity: {req.get('requested_quantity')} units")
            print(f"  Reason: {req.get('reason')}")
            print(f"  Submitted: {req.get('requested_at')}")
            
            if req.get('status') == 'approved':
                print(f"  ✓ APPROVED by Admin")
                print(f"    Approved: {req.get('approved_at')}")
            elif req.get('status') == 'rejected':
                print(f"  ✗ REJECTED by Admin")
                if req.get('admin_notes'):
                    print(f"    Reason: {req.get('admin_notes')}")
            else:
                print(f"  ⏳ PENDING Review")
        
        print("\n" + "-" * 80)
        print("\n✓ SUCCESS: Pharmacist portal can now display request status to pharmacist!")
        print("\nThis allows pharmacist to:")
        print("  - See all their submitted restock requests")
        print("  - Check if requests are pending, approved, or rejected")
        print("  - Read admin's feedback for rejected requests")
        print("  - Know when their request was approved and stock was added")
        
    else:
        print(f"✗ Error: {resp.json().get('message')}")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
