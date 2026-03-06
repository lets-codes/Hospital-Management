import requests
BASE='http://localhost:5000'

# These IDs assume previous quick test: user_id 101 and med_id 41
user_id = 101
med_id = 41

print('Deleting medicine', med_id, 'as pharmacist', user_id)
r = requests.delete(f"{BASE}/api/medicines/{med_id}", json={'actor_id': user_id}, timeout=5)
print('Status:', r.status_code, r.text)

# Confirm deletion
r2 = requests.get(f"{BASE}/api/medicines", timeout=5)
print('GET medicines status:', r2.status_code)
if r2.status_code==200:
    meds = r2.json().get('medicines', [])
    ids = [m.get('id') for m in meds]
    print('Medicine present after delete?', med_id in ids)
else:
    print('Could not list medicines')
