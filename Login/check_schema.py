#!/usr/bin/env python3
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='deepanshu'
)

cursor = conn.cursor()

print('\n=== Database Schema ===\n')

# Check patient_alerts table
print('patient_alerts columns:')
try:
    cursor.execute("DESCRIBE patient_alerts")
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]}')
except Exception as e:
    print(f'  ERROR: {e}')

# Check follow_ups table  
print('\nfollow_ups columns:')
try:
    cursor.execute("DESCRIBE follow_ups")
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]}')
except Exception as e:
    print(f'  ERROR: {e}')

# Check lab_results table
print('\nlab_results columns:')
try:
    cursor.execute("DESCRIBE lab_results")
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]}')
except Exception as e:
    print(f'  ERROR: {e}')

# Check appointment_reschedules table
print('\nappointment_reschedules columns:')
try:
    cursor.execute("DESCRIBE appointment_reschedules")
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]}')
except Exception as e:
    print(f'  ERROR: {e}')

cursor.close()
conn.close()
