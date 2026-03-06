import requests, json
BASE='http://localhost:5000'
payload = {
    "patient_id": 1,
    "doctor_id": 2,
    "symptoms": "test auto-decrement",
    "diagnosis": "test",
    "medicine_name": "Paracetamol",
    "dosage": "500mg",
    "quantity": 3
}
print('POST /add-consultation payload:', payload)
try:
    r = requests.post(f"{BASE}/add-consultation", json=payload, timeout=10)
    print('POST status:', r.status_code)
    try:
        print('POST response JSON:')
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print('POST response text:')
        print(r.text)
except Exception as e:
    print('POST request failed:', e)

print('\nGET /api/medicines snapshot:')
try:
    r2 = requests.get(f"{BASE}/api/medicines", timeout=10)
    print('GET status:', r2.status_code)
    try:
        data = r2.json()
        print(json.dumps(data, indent=2))
    except Exception:
        print(r2.text)
except Exception as e:
    print('GET request failed:', e)
