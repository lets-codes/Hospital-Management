#!/usr/bin/env python3
"""
Fix database schema to support pharmacist role
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
    print("UPDATING DATABASE SCHEMA - ADDING PHARMACIST ROLE")
    print("=" * 80)
    print()
    
    print("Current role ENUM: ('patient','doctor','admin')")
    print("New role  ENUM: ('patient','doctor','admin','pharmacist')")
    print()
    
    # Modify the role column to include pharmacist
    print("Executing ALTER TABLE...")
    cursor.execute("""
        ALTER TABLE login MODIFY COLUMN role ENUM('patient','doctor','admin','pharmacist') DEFAULT 'patient'
    """)
    
    conn.commit()
    
    print("✓ Database schema updated successfully!")
    print()
    print("The login table now supports:")
    print("  - patient")
    print("  - doctor")
    print("  - admin")
    print("  - pharmacist")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import sys
    sys.exit(1)
