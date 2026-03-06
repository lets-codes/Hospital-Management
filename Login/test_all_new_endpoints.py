#!/usr/bin/env python3
"""
Comprehensive test of all new endpoints
Tests medicines CRUD and admin management endpoints
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"
TEST_RESULTS = []

def test_endpoint(name, method, endpoint, data=None, expected_status=200):
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            resp = requests.get(url, timeout=3)
        elif method == "POST":
            resp = requests.post(url, json=data, timeout=3)
        elif method == "PUT":
            resp = requests.put(url, json=data, timeout=3)
        elif method == "DELETE":
            resp = requests.delete(url, timeout=3)
        
        success = resp.status_code == expected_status
        status_text = "PASS" if success else "FAIL"
        
        result = {
            "test": name,
            "status": status_text,
            "method": method,
            "endpoint": endpoint,
            "http_status": resp.status_code,
            "expected": expected_status,
            "response": resp.text[:200] if resp.text else "(empty)"
        }
        
        TEST_RESULTS.append(result)
        
        print(f"[{status_text}] {method} {endpoint} -> HTTP {resp.status_code}")
        if not success:
            print(f"      Expected {expected_status}, got {resp.status_code}")
            if resp.text:
                print(f"      Response: {resp.text[:100]}")
        
        return resp
        
    except Exception as e:
        TEST_RESULTS.append({
            "test": name,
            "status": "ERROR",
            "method": method,
            "endpoint": endpoint,
            "error": str(e)
        })
        print(f"[ERROR] {method} {endpoint} -> {str(e)}")
        return None

def main():
    print("=" * 70)
    print("HOSPITAL MANAGEMENT SYSTEM - ENDPOINT TEST SUITE")
    print("=" * 70)
    print()
    
    # Wait for server
    print("Waiting for server to be ready...")
    for attempt in range(10):
        try:
            resp = requests.get(f"{BASE_URL}/health", timeout=1)
            print(f"Server is ready! ({resp.status_code})")
            break
        except:
            print(f"  Attempt {attempt+1}/10 - server not ready yet...")
            time.sleep(0.5)
    
    print()
    print("Testing MEDICINES endpoints:")
    print("-" * 70)
    
    # Test GET medicines (should be empty or have sample data)
    resp = test_endpoint(
        "GET medicines list",
        "GET",
        "/api/medicines",
        expected_status=200
    )
    
    # Test POST new medicine
    med_data = {
        "name": "Test Medicine",
        "generic_name": "testmed",
        "dosage": "500mg",
        "quantity": 100,
        "unit_price": 10.50,
        "manufacturer": "Test Corp"
    }
    
    resp = test_endpoint(
        "POST new medicine (should fail - no auth)",
        "POST",
        "/api/medicines",
        data=med_data,
        expected_status=403  # Expect 403 unauthorized without role
    )
    
    print()
    print("Testing ADMIN endpoints:")
    print("-" * 70)
    
    # Test GET admin users  
    resp = test_endpoint(
        "GET admin users",
        "GET",
        "/api/admin/users?actor_id=1",
        expected_status=200
    )
    
    # Test other endpoints that should exist
    test_endpoint(
        "GET admin settings",
        "GET",
        "/api/admin/settings",
        expected_status=200
    )
    
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in TEST_RESULTS if r.get("status") == "PASS")
    failed = sum(1 for r in TEST_RESULTS if r.get("status") == "FAIL")
    errors = sum(1 for r in TEST_RESULTS if r.get("status") == "ERROR")
    
    print(f"Total Tests: {len(TEST_RESULTS)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print()
    
    if errors > 0:
        print("WARNING: Some tests encountered errors (server may not be running)")
    
    return 0 if (failed == 0 and errors == 0) else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
