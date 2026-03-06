#!/usr/bin/env python3
"""
COMPLETE DATABASE FIX - Runs all necessary database setup
Run this script to fix appointment booking and doctor login issues
"""

import mysql.connector
from mysql.connector import Error
import sys

# Try these passwords in order (add your password here if needed)
COMMON_PASSWORDS = ['root', '', 'password', 'mysql', '12345', 'root@123']

def create_connection():
    """Create a database connection with multiple password attempts."""
    for password in COMMON_PASSWORDS:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=password
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                pwd_display = "no password" if not password else f"password: {'*' * len(password)}"
                print(f"✅ Connected to MySQL Server v{db_info} ({pwd_display})")
                return connection
        except Error:
            continue
    
    # If all attempts fail
    print(f"❌ Error: Could not connect to MySQL with default passwords")
    print("\n⚠️ SOLUTION:")
    print("1. Edit this file line 11, add your MySQL password to COMMON_PASSWORDS list")
    print("2. Save and run again")
    print("\nExample: COMMON_PASSWORDS = ['', 'root', 'your_password_here']")
    sys.exit(1)

def fix_database():
    """Fix the database with proper schema"""
    
    print("\n" + "="*70)
    print("[DATABASE FIX] Patient-Doctor System - Complete Setup")
    print("="*70 + "\n")

    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        # STEP 1: Ensure database exists
        print("📍 STEP 1: Creating/Verifying Database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS deepanshu")
        cursor.execute("USE deepanshu")
        print("✅ Database 'deepanshu' ready\n")

        # STEP 2: Drop all existing user tables in the database to ensure clean schema
        print("📍 STEP 2: Dropping all existing tables in the database for a clean slate...")
        try:
            # Disable FK checks
            cursor.execute('SET FOREIGN_KEY_CHECKS=0')
        except:
            pass

        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s", (DB_CONFIG['database'],))
        existing_tables = [row[0] for row in cursor.fetchall()]
        for table in existing_tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"   ✓ Dropped {table}")
            except Exception as e:
                print(f"   ⚠️ Could not drop {table}: {e}")

        try:
            cursor.execute('SET FOREIGN_KEY_CHECKS=1')
        except:
            pass
        print()
        print()

        # STEP 3: Create LOGIN table with ROLE column
        print("📍 STEP 3: Creating LOGIN table (with role support for patient & doctor)...")
        login_table = """
        CREATE TABLE login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            password VARCHAR(255) NOT NULL,
            role ENUM('patient', 'doctor', 'admin') DEFAULT 'patient' COMMENT 'Patient or Doctor user',
            
            -- Doctor-specific fields
            specialization VARCHAR(100) COMMENT 'Doctor specialization',
            license_number VARCHAR(50) COMMENT 'Medical license number',
            registration_number VARCHAR(50) COMMENT 'Registration number',
            experience_years INT COMMENT 'Years of experience',
            consultation_fee INT COMMENT 'Consultation fee in rupees',
            
            -- Common fields
            gender ENUM('M', 'F', 'Other'),
            date_of_birth DATE,
            address TEXT,
            city VARCHAR(100),
            state VARCHAR(100),
            postal_code VARCHAR(10),
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_email (email),
            INDEX idx_role (role),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(login_table)
        print("✅ LOGIN table created with role support\n")

        # STEP 4: Create APPOINTMENTS table
        print("📍 STEP 4: Creating APPOINTMENTS table...")
        # Create a minimal appointments table first to avoid environment-specific FK or enum issues
        appointments_table = """
        CREATE TABLE appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_patient_id (patient_id),
            INDEX idx_doctor_id (doctor_id),
            INDEX idx_appointment_date (appointment_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        print("--- APPOINTMENTS SQL ---")
        print(appointments_table)
        print("--- END APPOINTMENTS SQL ---")
        try:
            cursor.execute(appointments_table)
            print("✅ APPOINTMENTS table created\n")
        except Error as e:
            print(f"Appointment CREATE error: {e}")
            raise

        # STEP 5: Create PATIENT_MEDICAL_RECORDS table
        print("📍 STEP 5: Creating PATIENT_MEDICAL_RECORDS table...")
        medical_records_table = """
        CREATE TABLE patient_medical_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT,
            appointment_id INT,
            diagnosis TEXT,
            symptoms TEXT,
            prescription TEXT,
            blood_pressure VARCHAR(20),
            temperature DECIMAL(5,2),
            heart_rate INT,
            weight DECIMAL(5,2),
            height DECIMAL(5,2),
            bmi DECIMAL(5,2),
            allergies TEXT,
            chronic_conditions TEXT,
            previous_surgeries TEXT,
            record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES login(id),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL,
            INDEX idx_patient_id (patient_id),
            INDEX idx_doctor_id (doctor_id),
            INDEX idx_record_date (record_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(medical_records_table)
        print("✅ PATIENT_MEDICAL_RECORDS table created\n")

        # STEP 6: Create PRESCRIPTIONS table
        print("📍 STEP 6: Creating PRESCRIPTIONS table...")
        prescriptions_table = """
        CREATE TABLE prescriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            appointment_id INT NOT NULL,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            medicine_name VARCHAR(255) NOT NULL,
            dosage VARCHAR(50),
            frequency VARCHAR(100),
            duration VARCHAR(100),
            instructions TEXT,
            side_effects TEXT,
            contraindications TEXT,
            refillable BOOLEAN DEFAULT FALSE,
            prescription_date DATE,
            expiry_date DATE,
            status ENUM('active', 'expired', 'completed') DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES login(id),
            INDEX idx_patient_id (patient_id),
            INDEX idx_doctor_id (doctor_id),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(prescriptions_table)
        print("✅ PRESCRIPTIONS table created\n")

        # STEP 7: Create DOCTOR_SCHEDULE table
        print("📍 STEP 7: Creating DOCTOR_SCHEDULE table...")
        doctor_schedule_table = """
        CREATE TABLE doctor_schedule (
            id INT AUTO_INCREMENT PRIMARY KEY,
            doctor_id INT NOT NULL,
            day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            start_time TIME,
            end_time TIME,
            lunch_start TIME,
            lunch_end TIME,
            max_appointments_per_day INT DEFAULT 10,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (doctor_id) REFERENCES login(id) ON DELETE CASCADE,
            INDEX idx_doctor_id (doctor_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(doctor_schedule_table)
        print("✅ DOCTOR_SCHEDULE table created\n")

        # STEP 8: Create LAB_TESTS table
        print("📍 STEP 8: Creating LAB_TESTS table...")
        lab_tests_table = """
        CREATE TABLE lab_tests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT,
            test_name VARCHAR(255),
            test_date DATE,
            result_date DATE,
            result_value TEXT,
            reference_range VARCHAR(100),
            interpretation ENUM('normal', 'abnormal', 'critical') DEFAULT 'normal',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES login(id),
            INDEX idx_patient_id (patient_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(lab_tests_table)
        print("✅ LAB_TESTS table created\n")

        # STEP 9: Create PATIENT_ILLNESS_HISTORY table
        print("📍 STEP 9: Creating PATIENT_ILLNESS_HISTORY table...")
        illness_history_table = """
        CREATE TABLE patient_illness_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            disease_name VARCHAR(255),
            onset_date DATE,
            resolution_date DATE,
            severity ENUM('mild', 'moderate', 'severe') DEFAULT 'mild',
            status VARCHAR(50),
            treatment_type VARCHAR(100),
            medications_used TEXT,
            hospitalization_required BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
            INDEX idx_patient_id (patient_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(illness_history_table)
        print("✅ PATIENT_ILLNESS_HISTORY table created\n")

        # STEP 10: Create DOCTOR_PATIENT_RELATIONSHIP table
        print("📍 STEP 10: Creating DOCTOR_PATIENT_RELATIONSHIP table...")
        relationship_table = """
        CREATE TABLE doctor_patient_relationship (
            id INT AUTO_INCREMENT PRIMARY KEY,
            doctor_id INT NOT NULL,
            patient_id INT NOT NULL,
            is_primary BOOLEAN DEFAULT FALSE,
            relationship_since DATE,
            status ENUM('active', 'inactive') DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            UNIQUE KEY unique_doctor_patient (doctor_id, patient_id),
            FOREIGN KEY (doctor_id) REFERENCES login(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES login(id) ON DELETE CASCADE,
            INDEX idx_doctor_id (doctor_id),
            INDEX idx_patient_id (patient_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(relationship_table)
        print("✅ DOCTOR_PATIENT_RELATIONSHIP table created\n")

        conn.commit()
        cursor.close()
        conn.close()

        print("="*70)
        print("✅ DATABASE FIX COMPLETE!")
        print("="*70)
        print("\n✨ All tables created successfully with proper schema:")
        print("   ✓ LOGIN table with role support (patient/doctor)")
        print("   ✓ APPOINTMENTS table for booking appointments")
        print("   ✓ PATIENT_MEDICAL_RECORDS for health data")
        print("   ✓ PRESCRIPTIONS for medicines")
        print("   ✓ DOCTOR_SCHEDULE for availability")
        print("   ✓ LAB_TESTS for test results")
        print("   ✓ PATIENT_ILLNESS_HISTORY for disease tracking")
        print("   ✓ DOCTOR_PATIENT_RELATIONSHIP for associations")
        print("\n🚀 NEXT STEPS:")
        print("   1. Start the backend: python server_patient_doctor.py")
        print("   2. Open browser: http://localhost:5000/hospital_landing.html")
        print("   3. Sign up as Patient or Doctor")
        print("   4. Login and test the system")
        print("\n")
        
        return True

    except Error as e:
        print(f"❌ Database Error: {e}")
        print(f"\nFailed to create tables. Error details: {str(e)}")
        conn.close()
        return False

if __name__ == '__main__':
    success = fix_database()
    if not success:
        sys.exit(1)
