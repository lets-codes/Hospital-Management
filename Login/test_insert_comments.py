#!/usr/bin/env python3
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='deepanshu'
)

cursor = conn.cursor()

# Try direct INSERT
sql = """
INSERT INTO patient_medical_records 
(patient_id, doctor_id, appointment_id, symptoms, diagnosis, comments)
VALUES (%s, %s, %s, %s, %s, %s)
"""

params = (10, 11, 3, 'Test symptoms', 'Test diagnosis', 'This is a test comment')

print(f"Executing: {sql}")
print(f"Params: {params}")

try:
    cursor.execute(sql, params)
    conn.commit()
    print(f"Successfully inserted, row ID: {cursor.lastrowid}")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()

# Now verify
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='deepanshu'
)

cursor = conn.cursor(dictionary=True)
cursor.execute(f"SELECT * FROM patient_medical_records WHERE id = {cursor.lastrowid if 'cursor' in locals() else 4}")
record = cursor.fetchone()
if record:
    print(f"\nVerify - Comments: {record.get('comments')}")
conn.close()
