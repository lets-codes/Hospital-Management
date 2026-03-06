#!/usr/bin/env python3
import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='', database='deepanshu')
cursor = conn.cursor(dictionary=True)
cursor.execute('SELECT comments FROM patient_medical_records WHERE id = 4')
record = cursor.fetchone()
if record:
    print(f'Comments in record 4: "{record.get("comments")}"')
else:
    print('Record 4 not found')
conn.close()
