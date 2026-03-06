#!/usr/bin/env python3
"""
Migrate Appointments Table - Add Missing Columns
Adds reason_for_visit and consultation_type columns to appointments table
"""

import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

def migrate_appointments_table():
    print("=" * 70)
    print("🔄 MIGRATING APPOINTMENTS TABLE")
    print("=" * 70)
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if columns exist
        cursor.execute("DESCRIBE appointments")
        columns = [row[0] for row in cursor.fetchall()]
        
        print("\n📋 Current appointments table columns:")
        for col in columns:
            print(f"   • {col}")
        
        # Add missing columns if not exist
        missing_columns = []
        
        if 'reason_for_visit' not in columns:
            missing_columns.append('reason_for_visit')
        if 'consultation_type' not in columns:
            missing_columns.append('consultation_type')
        if 'status' not in columns:
            missing_columns.append('status')
        
        if missing_columns:
            print(f"\n⚠️  Missing columns: {', '.join(missing_columns)}")
            print("\n🔧 Adding missing columns...")
            
            # Add reason_for_visit
            if 'reason_for_visit' not in columns:
                cursor.execute('''
                    ALTER TABLE appointments 
                    ADD COLUMN reason_for_visit TEXT 
                    AFTER appointment_time
                ''')
                print("   ✅ Added reason_for_visit column")
            
            # Add consultation_type
            if 'consultation_type' not in columns:
                cursor.execute('''
                    ALTER TABLE appointments 
                    ADD COLUMN consultation_type VARCHAR(50) DEFAULT 'in-person'
                    AFTER reason_for_visit
                ''')
                print("   ✅ Added consultation_type column")
            
            # Add status
            if 'status' not in columns:
                cursor.execute('''
                    ALTER TABLE appointments 
                    ADD COLUMN status VARCHAR(50) DEFAULT 'scheduled'
                    AFTER consultation_type
                ''')
                print("   ✅ Added status column")
            
            conn.commit()
            print("\n✅ Migration completed successfully!")
        else:
            print("\n✅ All required columns already exist!")
        
        # Verify final structure
        print("\n📋 Final appointments table structure:")
        cursor.execute("DESCRIBE appointments")
        for row in cursor.fetchall():
            print(f"   • {row[0]}: {row[1]}")
        
        print("\n" + "=" * 70)
        print("✅ APPOINTMENTS TABLE MIGRATION COMPLETE")
        print("=" * 70)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Migration Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    migrate_appointments_table()
