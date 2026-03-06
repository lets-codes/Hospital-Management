#!/usr/bin/env python3
"""Check what routes are registered with Flask"""
import sys
sys.path.insert(0, 'd:\\Storage Box\\Computer Input\\Visual Studio\\Project\\Shivani Anand\\Hospital Management\\Login')

from server_patient_doctor import app

print("Registered Flask Routes:")
print("="*60)
for rule in app.url_map.iter_rules():
    print(f"{rule.rule:40} {list(rule.methods)}")
print("="*60)
