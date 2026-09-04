import requests, uuid
BASE = 'http://localhost:5000'
email = f'lab_{uuid.uuid4().hex[:8]}@test.com'
s = requests.post(BASE + '/signup', json={'fullname': 'Lab Tech New', 'email': email, 'phone': '7777777777', 'password': 'lab12345', 'role': 'lab'}, timeout=10)
print('signup', s.status_code, s.text)
if s.status_code != 201:
    raise SystemExit(1)
user = s.json()
lab_id = user['user_id']
p = requests.post(BASE + '/signup', json={'fullname': 'Patient Lab Link', 'email': f'patient_{uuid.uuid4().hex[:8]}@test.com', 'phone': '1234567890', 'password': 'patient123', 'role': 'patient'}, timeout=10)
print('patient', p.status_code, p.text)
if p.status_code != 201:
    raise SystemExit(1)
patient_id = p.json()['user_id']
r = requests.post(BASE + '/api/lab-result', json={'actor_id': lab_id, 'patient_id': patient_id, 'doctor_id': lab_id, 'test_name': 'CBC', 'result_value': '5.2', 'result_unit': 'mmol/L', 'reference_range': '3.5-5.5', 'status': 'normal', 'notes': 'All fine'}, timeout=10)
print('lab_result', r.status_code, r.text)
if r.status_code != 201:
    raise SystemExit(1)
results = requests.get(f'{BASE}/api/lab-results/{patient_id}', timeout=10)
print('results', results.status_code, results.text[:500])
if results.status_code != 200:
    raise SystemExit(1)
patients = requests.get(f'{BASE}/api/lab/patients', params={'actor_id': lab_id}, timeout=10)
print('patients', patients.status_code, patients.text[:300])
if patients.status_code != 200:
    raise SystemExit(1)
