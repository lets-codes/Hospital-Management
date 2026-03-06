#!/usr/bin/env python3
"""Smoke test: insert a medicine directly into DB and query the API list"""
import time
import mysql.connector
import requests

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

def ensure_sample_medicine():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Insert a sample medicine if not exists
        name = 'TestMed-A'
        cursor.execute('SELECT id FROM medicines WHERE name = %s', (name,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO medicines (name, sku, manufacturer, quantity, unit_price) VALUES (%s,%s,%s,%s,%s)',
                           (name, 'TST-A', 'Acme Pharma', 25, 12.50))
            conn.commit()
            print('Inserted sample medicine')
        else:
            print('Sample medicine already exists')
        cursor.close()
        conn.close()
    except Exception as e:
        print('DB insert error:', e)


def list_medicines_via_api():
    try:
        url = 'http://127.0.0.1:5000/api/medicines'
        r = requests.get(url, timeout=5)
        print('API status:', r.status_code)
        print('Response JSON:', r.json())
    except Exception as e:
        print('API request error:', e)


if __name__ == '__main__':
    print('Waiting briefly for server to start...')
    time.sleep(2)
    ensure_sample_medicine()
    time.sleep(0.5)
    list_medicines_via_api()
