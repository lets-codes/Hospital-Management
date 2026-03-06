import requests
import threading
import time
import json

BASE = 'http://localhost:5000'

received = []

def sse_listener():
    try:
        with requests.get(f'{BASE}/stream', stream=True, timeout=30) as r:
            if r.status_code != 200:
                print('SSE connection failed, status:', r.status_code)
                return
            print('SSE connected, listening...')
            buffer = ''
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    line = line.strip()
                    if line.startswith('data:'):
                        payload = line[len('data:'):].strip()
                        try:
                            ev = json.loads(payload)
                        except Exception:
                            ev = {'raw': payload}
                        print('EVENT:', ev)
                        received.append(ev)
                        # Stop after first event
                        return
    except Exception as e:
        print('SSE listener error:', e)

# Start listener thread
t = threading.Thread(target=sse_listener, daemon=True)
print('Starting SSE listener thread...')
t.start()

# Give listener time to connect
time.sleep(1)

# Trigger action: add a medicine
print('Posting new medicine to trigger SSE...')
try:
    resp = requests.post(f'{BASE}/api/medicines', json={
        'actor_id': 102,
        'name': 'SSE Test Medicine',
        'quantity': 5,
        'unit_price': 10.0
    }, timeout=5)
    print('POST status:', resp.status_code, resp.text)
except Exception as e:
    print('POST error:', e)

# Wait for event or timeout
start = time.time()
while time.time() - start < 10 and not received:
    time.sleep(0.2)

if not received:
    print('No SSE events received within timeout')
else:
    print('Received events count:', len(received))

print('Done')
