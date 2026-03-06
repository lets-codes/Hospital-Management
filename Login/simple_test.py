#!/usr/bin/env python3
"""Simple test"""

import requests

response = requests.options('http://localhost:5000/add-lab-result', timeout=5)
print(f"Status: {response.status_code}")
print(f"Allow: {response.headers.get('Allow', 'NOT SET')}")
