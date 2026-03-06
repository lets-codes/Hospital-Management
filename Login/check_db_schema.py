#!/usr/bin/env python3
"""
Check database schema for login table
"""
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("CHECKING LOGIN TABLE SCHEMA")
    print("=" * 80)
    print()
    
    # Get table structure
    cursor.execute("DESCRIBE login")
    columns = cursor.fetchall()
    
    for col in columns:
        print(f"Column: {col[0]:20s} | Type: {col[1]:30s} | Null: {col[2]:5s} | Key: {col[3]:5s} | Default: {col[4]} | Extra: {col[5]}")
    
    print()
    print("=" * 80)
    print("CHECKING UNIQUE ROLES IN DATABASE")
    print("=" * 80)
    print()
    
    cursor.execute("SELECT DISTINCT role FROM login WHERE role IS NOT NULL AND role != '' ORDER BY role")
    roles = cursor.fetchall()
    
    for role in roles:
        cursor.execute(f"SELECT COUNT(*) FROM login WHERE role = %s", (role[0],))
        count = cursor.fetchone()[0]
        print(f"Role: {role[0]:15s} | Count: {count}")
    
    cursor.execute("SELECT COUNT(*) FROM login WHERE role IS NULL OR role = ''")
    empty = cursor.fetchone()[0]
    print(f"Role: {'(empty)':15s} | Count: {empty}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
