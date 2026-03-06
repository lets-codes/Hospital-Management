import requests
BASE='http://localhost:5000'
print('Updating med 41 quantity to 5 as user 101')
r = requests.put(f'{BASE}/api/medicines/41', json={'actor_id':101,'quantity':5}, timeout=5)
print(r.status_code, r.text)
