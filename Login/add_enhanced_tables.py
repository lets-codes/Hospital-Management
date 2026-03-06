#!/usr/bin/env python3
"""
Add new tables for enhanced features:
- Lab test results
- Patient alerts/flags  
- Follow-up schedules
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

def add_new_tables():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check and create lab_results table
        print("Checking lab_results table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lab_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                doctor_id INT,
                test_name VARCHAR(100) NOT NULL,
                test_date DATE,
                result_value VARCHAR(255),
                result_unit VARCHAR(50),
                reference_range VARCHAR(100),
                status VARCHAR(50),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES login(id),
                INDEX idx_patient_id (patient_id),
                INDEX idx_test_date (test_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ lab_results table ready")
        
        # Check and create patient_alerts table
        print("Checking patient_alerts table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                alert_type VARCHAR(50),
                alert_title VARCHAR(255) NOT NULL,
                alert_message TEXT,
                severity VARCHAR(50),
                is_read BOOLEAN DEFAULT FALSE,
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES login(id),
                INDEX idx_patient_id (patient_id),
                INDEX idx_severity (severity)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ patient_alerts table ready")
        
        # Check and create follow_ups table
        print("Checking follow_ups table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS follow_ups (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                doctor_id INT NOT NULL,
                original_appointment_id INT,
                follow_up_date DATE NOT NULL,
                follow_up_time TIME,
                reason VARCHAR(255),
                status VARCHAR(50) DEFAULT 'scheduled',
                notes TEXT,
                scheduled_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES login(id),
                FOREIGN KEY (original_appointment_id) REFERENCES appointments(id),
                FOREIGN KEY (scheduled_by) REFERENCES login(id),
                INDEX idx_patient_id (patient_id),
                INDEX idx_doctor_id (doctor_id),
                INDEX idx_follow_up_date (follow_up_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ follow_ups table ready")
        
        # Check and create appointment_rescheduling table
        print("Checking appointment_rescheduling table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointment_reschedules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                original_appointment_id INT NOT NULL,
                patient_id INT NOT NULL,
                old_date DATE,
                old_time TIME,
                new_date DATE,
                new_time TIME,
                reason VARCHAR(255),
                rescheduled_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (original_appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
                FOREIGN KEY (patient_id) REFERENCES login(id),
                FOREIGN KEY (rescheduled_by) REFERENCES login(id),
                INDEX idx_patient_id (patient_id),
                INDEX idx_new_date (new_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ appointment_reschedules table ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ All new tables created successfully!")
        print("="*60)
        print("\nNew tables available:")
        print("  1. lab_results - Store patient lab test results")
        print("  2. patient_alerts - Create alerts for patient conditions")
        print("  3. follow_ups - Schedule follow-up appointments")
        print("  4. appointment_reschedules - Track rescheduled appointments")
        return True
        
    except Error as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  ADDING ENHANCED FEATURE TABLES")
    print("="*60)
    add_new_tables()
