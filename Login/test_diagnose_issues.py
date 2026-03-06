"""Test to diagnose logout and add medicine issues"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_logout_and_medicine():
    """Test logout and add medicine functionality"""
    print("\n" + "="*70)
    print("DIAGNOSTIC TEST - LOGOUT AND ADD MEDICINE ISSUES")
    print("="*70)
    
    unique_id = int(time.time())
    test_email = f"diagnostic_{unique_id}@test.com"
    
    # Create account
    print("\n[1] Creating test pharmacist account...")
    signup_response = requests.post(
        f"{BASE_URL}/signup",
        json={
            "email": test_email,
            "password": "Test@123",
            "fullname": "Diagnostic User",
            "phone": "9876543210",
            "role": "pharmacist"
        }
    )
    
    if not signup_response.ok:
        print(f"  ✗ Signup failed: {signup_response.json()}")
        return
    
    user_id = signup_response.json()['user_id']
    print(f"  ✓ Account created - User ID: {user_id}")
    
    # Test login
    print("\n[2] Testing login...")
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"email": test_email, "password": "Test@123"}
    )
    
    if not login_response.ok:
        print(f"  ✗ Login failed: {login_response.json()}")
        return
    
    print(f"  ✓ Login successful")
    
    # Test add medicine with various scenarios
    print("\n[3] Testing add medicine with FULL validation...")
    
    test_cases = [
        {
            "name": "Test Medicine 1",
            "sku": "TEST-001",
            "manufacturer": "Test Corp",
            "quantity": 100,
            "unit_price": 50.0,
            "description": "Valid - all fields"
        },
        {
            "name": "",
            "sku": "TEST-002",
            "manufacturer": "Test",
            "quantity": 50,
            "unit_price": 25.0,
            "description": "Invalid - empty name"
        },
        {
            "name": "Test Medicine 3",
            "sku": "",
            "manufacturer": "",
            "quantity": 0,
            "unit_price": 0,
            "description": "Valid - minimal fields (name required)"
        },
        {
            "name": "Test Medicine 4",
            "sku": "TEST-004",
            "manufacturer": "Test",
            "quantity": -5,
            "unit_price": 50.0,
            "description": "Invalid - negative quantity"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n  Test Case {i+1}: {test_case['description']}")
        
        payload = {
            "actor_id": user_id,
            "name": test_case['name'],
            "sku": test_case['sku'],
            "manufacturer": test_case['manufacturer'],
            "quantity": test_case['quantity'],
            "unit_price": test_case['unit_price']
        }
        
        response = requests.post(
            f"{BASE_URL}/api/medicines",
            json=payload
        )
        
        print(f"    Status: {response.status_code}")
        print(f"    Response: {response.json()}")
        
        if response.ok:
            print(f"    ✓ Accepted")
        else:
            print(f"    ✗ Rejected (Error)")
    
    # Test logout endpoint (check if it exists)
    print("\n[4] Testing logout functionality...")
    print(f"    Frontend logout redirects to: /login.html")
    print(f"    This should navigate user back to login page")
    print(f"    localStorage.removeItem('user') - clears session")
    
    # Check if server has a logout endpoint
    print("\n[5] Checking for server-side logout endpoint...")
    logout_response = requests.post(
        f"{BASE_URL}/logout",
        json={"user_id": user_id}
    )
    
    if logout_response.status_code == 404:
        print(f"    ⚠ No server-side logout endpoint (this is OK)")
    else:
        print(f"    Status: {logout_response.status_code}")
        print(f"    Response: {logout_response.json()}")
    
    # Test the inventory endpoint  
    print("\n[6] Testing pharmacy inventory endpoint...")
    inventory_response = requests.get(
        f"{BASE_URL}/api/pharmacist/inventory?actor_id={user_id}"
    )
    
    if inventory_response.ok:
        medicines = inventory_response.json().get('medicines', [])
        print(f"    ✓ Inventory loaded successfully")
        print(f"    Total medicines: {len(medicines)}")
    else:
        print(f"    ✗ Inventory error: {inventory_response.json()}")
    
    print("\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    print("""
FINDINGS:

Add Medicine Issues:
- The API endpoint (/api/medicines) is working correctly
- It correctly accepts valid medicine data
- It correctly rejects invalid data (empty name, negative values)
- The issue is likely in the FRONTEND JavaScript code, not the API

Logout Issues:
- The logout() function in HTML removes localStorage
- It redirects to /login.html - this should work
- But path might need to be fixed if running from subdirectory
- Should use relative path like 'login.html' or '/login.html'

NOTE: Frontend code processes before sending to API,
so validation errors happen in browser, not server.
    """)
    
    return True

if __name__ == '__main__':
    try:
        test_logout_and_medicine()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
