import requests
from datetime import datetime

# Create a test account
doctor_data = {
    'role': 'doctor',
    'fullname': 'Dr. Test Fix',
    'email': f'drtestfix_{datetime.now().timestamp()}@test.com',
    'phone': '6666666666',
    'password': 'password123',
    'specialization': 'Medicine',
    'license_number': 'LIC333',
    'experience_years': 5,
    'consultation_fee': 500
}

BASE = 'http://localhost:5000'
r = requests.post(f'{BASE}/signup', json=doctor_data)
result = r.json()
if 'user_id' not in result:
    print(f'Signup failed: {result}')
    exit(1)
    
doctor_id = result['user_id']
print(f'Doctor created: {doctor_id}')

# Test the endpoint
r2 = requests.get(f'{BASE}/get-doctor-appointments/{doctor_id}')
print(f'Status: {r2.status_code}')
if r2.status_code == 200:
    data = r2.json()
    print(f'Today appointments: {len(data["today"])}')
    print(f'Upcoming appointments: {len(data["upcoming"])}')
    print('✓ FIXED!')
else:
    print(f'Error: {r2.text[:300]}')
