import requests, json
BASE='http://localhost:5000'

def fetch(url):
    try:
        r = requests.get(url, timeout=5)
        print(url, '->', r.status_code)
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text[:500])
    except Exception as e:
        print(url, 'error ->', repr(e))

if __name__=='__main__':
    fetch(f"{BASE}/api/notifications?role=admin&limit=5")
    fetch(f"{BASE}/api/admin/restock-requests")
    fetch(f"{BASE}/api/medicines")
