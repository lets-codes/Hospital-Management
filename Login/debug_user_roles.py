#!/usr/bin/env python3
"""
Debug script to check user roles in database
"""
import mysql.connector
import sys

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    print("=" * 80)
    print("DEBUG: CHECKING USER ROLES IN DATABASE")
    print("=" * 80)
    print()
    
    # Get all users with recent creation
    cursor.execute("SELECT id, full_name, email, role FROM login ORDER BY id DESC LIMIT 20")
    users = cursor.fetchall()
    
    print(f"Latest 20 users in database:")
    print("-" * 80)
    for user in users:
        print(f"ID: {user['id']:3d} | Role: {user['role']:12s} | Name: {user['full_name']:30s} | Email: {user['email']}")
    
    print()
    print("=" * 80)
    print(f"Test users created in recent tests:")
    print("-" * 80)
    
    # Look for test users
    cursor.execute("SELECT id, full_name, email, role FROM login WHERE email LIKE '%test%portal%' ORDER BY id DESC")
    test_users = cursor.fetchall()
    
    if test_users:
        for user in test_users:
            print(f"ID: {user['id']} | Role: {user['role']} | Name: {user['full_name']} | Email: {user['email']}")
    else:
        print("No test portal users found")
    
    cursor.close()
    conn.close()
    
    print()
    print("✓ Database check complete")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
