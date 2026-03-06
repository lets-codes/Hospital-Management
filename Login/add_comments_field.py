#!/usr/bin/env python3
"""
Add comments field to patient_medical_records table
"""
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='deepanshu'
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def add_comments_field():
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if column already exists
        print("📍 Checking if comments field exists...")
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'patient_medical_records' AND COLUMN_NAME = 'comments'
        """)
        
        if cursor.fetchone():
            print("✅ Comments field already exists")
            cursor.close()
            conn.close()
            return True
        
        print("📍 Adding comments field to patient_medical_records table...")
        cursor.execute("""
            ALTER TABLE patient_medical_records 
            ADD COLUMN comments TEXT AFTER diagnosis
        """)
        
        # Also add observations field for completeness
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'patient_medical_records' AND COLUMN_NAME = 'observations'
        """)
        
        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE patient_medical_records 
                ADD COLUMN observations TEXT AFTER comments
            """)
        
        conn.commit()
        
        # Verify
        print("📍 Verifying table structure...")
        cursor.execute("""
            DESCRIBE patient_medical_records
        """)
        
        columns = cursor.fetchall()
        print("\n✅ Updated patient_medical_records table structure:")
        print("─" * 60)
        for col in columns:
            print(f"   {col[0]:20} {col[1]:25}")
        print("─" * 60)
        
        cursor.close()
        conn.close()
        print("\n✅ Comments field added successfully!")
        return True
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  ADD COMMENTS FIELD TO PATIENT MEDICAL RECORDS")
    print("=" * 60)
    add_comments_field()
