import requests, json, datetime, time
BASE='http://localhost:5000'

session = requests.Session()

# Helper to create a user
def create_user(full_name, email, phone, password, role='patient', extra=None):
    payload = {'fullname': full_name, 'email': email, 'phone': phone, 'password': password, 'role': role}
    if extra:
        payload.update(extra)
    r = session.post(f"{BASE}/signup", json=payload, timeout=10)
    return r

# Create doctor
doc_email = f"test_doc_{int(time.time())}@test.local"
r = create_user('Test Doctor E2E', doc_email, '9999999999', 'password123', role='doctor', extra={'specialization':'General','license_number':'LIC123','experience_years':5,'consultation_fee':200})
print('Create doctor status', r.status_code, r.text)
if r.status_code not in (200,201):
    print('Doctor creation failed, abort')
    exit(1)
doc_id = r.json().get('user_id')

# Create patient
pat_email = f"test_patient_{int(time.time())}@test.local"
r = create_user('Test Patient E2E', pat_email, '8888888888', 'password123', role='patient')
print('Create patient status', r.status_code, r.text)
if r.status_code not in (200,201):
    print('Patient creation failed, abort')
    exit(1)
pat_id = r.json().get('user_id')

# Book appointment
appt_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
appt_time = '10:00'
payload = {'patient_id': pat_id, 'doctor_id': doc_id, 'appointment_date': appt_date, 'appointment_time': appt_time, 'reason_for_visit':'E2E test'}
r = session.post(f"{BASE}/book-appointment", json=payload, timeout=10)
print('Book appointment status', r.status_code, r.text)
if r.status_code not in (200,201):
    print('Appointment failed, abort')
    exit(1)

# Snapshot medicines before
r = session.get(f"{BASE}/api/medicines", timeout=10)
print('\nMedicines before: status', r.status_code)
meds = r.json().get('medicines', [])
# pick first with qty>0
med = next((m for m in meds if (m.get('quantity') or 0) > 0), None)
if not med:
    print('No medicine with positive stock found — creating a test medicine')
    # create a pharmacist user to add medicine
    pharm_email = f"test_pharm_{int(time.time())}@test.local"
    rph = create_user('Test Pharmacist E2E', pharm_email, '7777777777', 'password123', role='pharmacist')
    print('Create pharmacist status', rph.status_code, rph.text)
    pharm_id = rph.json().get('user_id')
    med_payload = {
        'actor_id': pharm_id,
        'name': 'E2E Test Medicine',
        'sku': 'E2E-001',
        'manufacturer': 'TestCo',
        'batch_no': 'BATCH-E2E',
        'expiry_date': None,
        'quantity': 10,
        'unit_price': 1.5
    }
    radd = session.post(f"{BASE}/api/medicines", json=med_payload, timeout=10)
    print('Add medicine status', radd.status_code, radd.text)
    if radd.status_code not in (200,201):
        print('Failed to add medicine, abort')
        exit(1)
    # reload medicines
    r = session.get(f"{BASE}/api/medicines", timeout=10)
    meds = r.json().get('medicines', [])
    med = next((m for m in meds if (m.get('quantity') or 0) > 0), None)
    if not med:
        print('Still no medicine with positive stock, abort')
        exit(1)
print(json.dumps(med, indent=2))

# Post consultation with quantity=2
payload = {
    'patient_id': pat_id,
    'doctor_id': doc_id,
    'symptoms': 'E2E symptoms',
    'diagnosis': 'E2E diag',
    'medicine_id': med.get('id'),
    'medicine_name': med.get('name'),
    'dosage': '1 tablet',
    'quantity': 2
}
print('\nPosting consultation payload:', payload)
r = session.post(f"{BASE}/add-consultation", json=payload, timeout=10)
print('Consultation POST status', r.status_code)
try:
    print(json.dumps(r.json(), indent=2))
except Exception:
    print('Response text:', r.text)

# Snapshot medicines after
r = session.get(f"{BASE}/api/medicines", timeout=10)
print('\nMedicines after: status', r.status_code)
meds_after = r.json().get('medicines', [])
med_after = next((m for m in meds_after if m.get('id') == med.get('id')), None)
print('After snapshot for same id:')
print(json.dumps(med_after, indent=2))

# Fetch prescriptions for the patient to verify
print('\nGET /get-prescriptions for patient:', pat_id)
rp = session.get(f"{BASE}/get-prescriptions/{pat_id}", timeout=10)
print('GET prescriptions status', rp.status_code)
try:
    print(json.dumps(rp.json(), indent=2))
except Exception:
    print('Prescriptions response text:', rp.text)
