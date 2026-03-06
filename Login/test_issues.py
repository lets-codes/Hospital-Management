"""Test script to identify signup/login and add medicine issues"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_signup_and_add_medicine():
    """Test signup and add medicine functionality"""
    print("\n" + "="*60)
    print("TESTING SIGNUP AND ADD MEDICINE ISSUES")
    print("="*60)
    
    # Test 1: Create a pharmacist account
    print("\n[TEST 1] Creating A Pharmacist Account...")
    signup_data = {
        "email": f"testpharma_{int(time.time())}@test.com",
        "password": "Test@1234",
        "fullname": "Test Pharmacist",
        "role": "pharmacist",
        "phone": "9999999999"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.ok:
            print("  ✓ Signup successful")
            
            # Test 2: Login with the account
            print("\n[TEST 2] Logging In...")
            login_response = requests.post(
                f"{BASE_URL}/login",
                json={"email": signup_data['email'], "password": signup_data['password']}
            )
            print(f"  Status: {login_response.status_code}")
            login_data = login_response.json()
            print(f"  Response: {login_data}")
            
            if login_response.ok and login_data.get('user'):
                user_id = login_data['user'].get('id')
                print(f"  ✓ Login successful - User ID: {user_id}")
                
                # Test 3: Add medicine
                print("\n[TEST 3] Adding A Medicine...")
                medicine_data = {
                    "actor_id": user_id,
                    "name": "Test Aspirin",
                    "sku": "ASP-TEST-001",
                    "manufacturer": "Test Pharma Corp",
                    "quantity": 100,
                    "unit_price": 50.0
                }
                
                med_response = requests.post(
                    f"{BASE_URL}/api/medicines",
                    json=medicine_data
                )
                print(f"  Status: {med_response.status_code}")
                print(f"  Response: {med_response.json()}")
                
                if med_response.ok:
                    print("  ✓ Medicine added successfully")
                else:
                    print(f"  ✗ Failed to add medicine: {med_response.json()}")
            else:
                print(f"  ✗ Login failed")
        else:
            print(f"  ✗ Signup failed: {response.json()}")
            
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_signup_and_add_medicine()
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")
