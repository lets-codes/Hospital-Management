#!/usr/bin/env python3
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='deepanshu'
)

cursor = conn.cursor(dictionary=True)
cursor.execute('SELECT * FROM patient_medical_records WHERE id = 3')
record = cursor.fetchone()
if record:
    print(f'Record 3:')
    print(f'  Diagnosis: {record.get("diagnosis")}')
    print(f'  Comments: {record.get("comments")}')
    print(f'  Symptoms: {record.get("symptoms")}')
else:
    print("Record 3 not found")
conn.close()
