#!/usr/bin/env python3
"""Add 30 non-expired medicines to the local database via the API.

This script creates a temporary pharmacist account (to satisfy permission checks)
and then adds 30 medicines with expiry dates in the future (non-expired).

Usage:
    python add_30_medicines.py

Requirements:
    - The Flask server must be running (default: http://localhost:5000)
    - The database must be accessible and the `medicines` table must exist

After running, you can verify the medicines list by visiting:
    http://localhost:5000/pharmacist_portal.html

"""

import json
import time
from datetime import datetime, timedelta, timezone

import requests

BASE_URL = 'http://localhost:5000'


def create_pharmacist():
    email = f"seed_pharm_{int(time.time())}@test.com"
    data = {
        'role': 'pharmacist',
        'fullname': 'Seed Pharmacist',
        'email': email,
        'phone': '9999999999',
        'password': 'SeedPass123!'
    }
    resp = requests.post(f"{BASE_URL}/signup", json=data)
    resp.raise_for_status()
    return resp.json().get('user_id'), email


def add_medicine(actor_id, name, quantity=10, unit_price=10.0, expiry_date='2027-12-31', batch_no=None, manufacturer='Seed Pharma'):
    payload = {
        'actor_id': actor_id,
        'name': name,
        'quantity': quantity,
        'unit_price': unit_price,
        'expiry_date': expiry_date,
        'manufacturer': manufacturer,
    }
    if batch_no:
        payload['batch_no'] = batch_no

    resp = requests.post(f"{BASE_URL}/api/medicines", json=payload)
    resp.raise_for_status()
    return resp.json().get('medicine_id')


def iso_date(days_offset: int) -> str:
    """Return a YYYY-MM-DD date string offset from today."""
    return (datetime.now(timezone.utc).date() + timedelta(days=days_offset)).isoformat()


def main():
    print("Creating pharmacist account (for API permission)...")
    pharm_id, pharm_email = create_pharmacist()
    print(f"  -> Pharmacist created: id={pharm_id}, email={pharm_email}")

    print("\nAdding 30 non-expired medicines...")
    created = []
    base_name = "SEED_MED_"
    for i in range(1, 31):
        name = f"{base_name}{i:02d}"
        batch = f"BATCH-{int(time.time())}-{i:02d}"
        qty = 10 + (i % 5) * 5
        price = 5.0 + (i % 8) * 2.5
        med_id = add_medicine(
            actor_id=pharm_id,
            name=name,
            quantity=qty,
            unit_price=round(price, 2),
            expiry_date='2027-12-31',
            batch_no=batch,
            manufacturer='SeedLabs'
        )
        created.append((med_id, name))
        print(f"  {i:02d}. Created medicine id={med_id} name={name}")
        time.sleep(0.05)

    print("\nAdding 15 expiring medicines (soon-to-expire)...")
    for i in range(1, 16):
        name = f"EXPIRING_MED_{i:02d}"
        batch = f"EXP-{int(time.time())}-{i:02d}"
        qty = 5 + (i % 4) * 5
        price = 3.0 + (i % 6) * 1.5
        expiry = iso_date(days_offset=30 + (i % 10))
        med_id = add_medicine(
            actor_id=pharm_id,
            name=name,
            quantity=qty,
            unit_price=round(price, 2),
            expiry_date=expiry,
            batch_no=batch,
            manufacturer='SeedLabs'
        )
        print(f"  EXP {i:02d}. Created expiring med id={med_id} name={name} expiry={expiry}")
        time.sleep(0.05)

    print("\nAdding 5 already expired medicines...")
    for i in range(1, 6):
        name = f"EXPIRED_MED_{i:02d}"
        batch = f"EXP-D-{int(time.time())}-{i:02d}"
        qty = 2 + i
        price = 2.0 + i
        expiry = iso_date(days_offset=-7 - i)
        med_id = add_medicine(
            actor_id=pharm_id,
            name=name,
            quantity=qty,
            unit_price=round(price, 2),
            expiry_date=expiry,
            batch_no=batch,
            manufacturer='SeedLabs'
        )
        print(f"  EXPD {i:02d}. Created expired med id={med_id} name={name} expiry={expiry}")
        time.sleep(0.05)

    print("\nDone. Created 50 medicines (30 normal, 15 expiring, 5 expired).\n")
    print("You can verify by visiting:")
    print("  http://localhost:5000/pharmacist_portal.html")
    print("Or via API:")
    print(f"  curl {BASE_URL}/api/medicines")


if __name__ == '__main__':
    main()
