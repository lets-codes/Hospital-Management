#!/usr/bin/env python3
"""Debug script to check what's in the database"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='deepanshu'
)

cursor = conn.cursor(dictionary=True)

# Check patient 10
print("Patient ID 10 data:")
cursor.execute("SELECT * FROM patient_medical_records WHERE patient_id = 10")
records = cursor.fetchall()
print(f"Medical records found: {len(records)}")
for record in records:
    print(f"  ID: {record.get('id')}, Doctor: {record.get('doctor_id')}, Comments: {record.get('comments')}")

# Check consultations for patient 10
print("\nConsultations for patient 10:")
cursor.execute("""
    SELECT pmr.*, l.full_name as doctor_name 
    FROM patient_medical_records pmr
    LEFT JOIN login l ON pmr.doctor_id = l.id
    WHERE pmr.patient_id = 10
""")
consultations = cursor.fetchall()
print(f"Consultations found: {len(consultations)}")
for cons in consultations:
    print(f"  Doctor: {cons.get('doctor_name')}")
    print(f"  Diagnosis: {cons.get('diagnosis')}")
    print(f"  Comments: {cons.get('comments')}")

# Check prescriptions
print("\nPrescriptions for patient 10:")
cursor.execute("SELECT * FROM prescriptions WHERE patient_id = 10")
prescriptions = cursor.fetchall()
print(f"Prescriptions found: {len(prescriptions)}")
for rx in prescriptions:
    print(f"  Medicine: {rx.get('medicine_name')}")

conn.close()
