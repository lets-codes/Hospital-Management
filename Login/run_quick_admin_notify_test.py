import requests
import time
import sys

BASE = 'http://localhost:5000'

def main():
    ts = int(time.time())
    email = f"pharm_{ts}@example.local"
    signup = {
        'role': 'pharmacist',
        'fullname': f'Test Pharmacist {ts}',
        'email': email,
        'phone': '9999999999',
        'password': 'password123'
    }
    try:
        r = requests.post(f"{BASE}/signup", json=signup, timeout=5)
    except Exception as e:
        print('ERROR: cannot reach server:', e)
        sys.exit(2)

    print('SIGNUP', r.status_code, r.text)
    if r.status_code not in (200,201):
        print('Signup failed; aborting')
        sys.exit(1)

    user_id = r.json().get('user_id')
    if not user_id:
        print('No user_id returned; aborting')
        sys.exit(1)

    med = {
        'actor_id': user_id,
        'name': f'AutoTestMed {ts}',
        'sku': f'ATM-{ts}',
        'manufacturer': 'TestCo',
        'quantity': 25,
        'unit_price': 19.99
    }

    r2 = requests.post(f"{BASE}/api/medicines", json=med, timeout=5)
    print('ADD MEDICINE', r2.status_code, r2.text)

    r3 = requests.get(f"{BASE}/api/medicines", timeout=5)
    print('GET MEDICINES', r3.status_code)
    if r3.status_code == 200:
        meds = r3.json().get('medicines', [])
        names = [m.get('name') for m in meds]
        print('Total medicines:', len(meds))
        print('Recent names (last 10):', names[-10:])
    else:
        print('Failed to list medicines:', r3.text)

if __name__ == '__main__':
    main()
