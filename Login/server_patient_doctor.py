#!/usr/bin/env python3
"""
Patient-Doctor Healthcare System Server
Comprehensive Flask backend with role-based functionality
"""

from flask import Flask, request, jsonify, send_file, render_template_string, Response, stream_with_context
from flask_cors import CORS
import mysql.connector
import bcrypt
import json
import secrets
import string
from datetime import datetime, timedelta, date
import os
import queue
import threading
import time

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app, origins=['*'])

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

# Try these passwords if initial one fails
BACKUP_PASSWORDS = ['', 'root', 'password', 'mysql', '12345', 'root@123']

def get_db_connection():
    """Create database connection with password fallback"""
    # Try main password first
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as first_error:
        if '1045' not in str(first_error):  # Not a password error
            print(f"Database Error during connection: {first_error}")
            return None
        
        # Try backup passwords
        for pwd in BACKUP_PASSWORDS:
            try:
                config = DB_CONFIG.copy()
                config['password'] = pwd
                conn = mysql.connector.connect(**config)
                print(f"[Connected with fallback password]")
                return conn
            except:
                continue
        
        # Show full error if all attempts fail
        print(f"Database Error during signup: {first_error}")
        return None

def validate_email(email):
    """Validate email format"""
    import re
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

def validate_password(password):
    """Validate password length"""
    return password and len(password) >= 6

# ============ AUTHENTICATION ENDPOINTS ============

@app.route('/signup', methods=['POST'])
def signup():
    """Register new user (Patient, Doctor, Pharmacist, or Admin)"""
    try:
        data = request.json
        role = data.get('role', 'patient').strip().lower()
        fullname = data.get('fullname', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        password = data.get('password', '')

        # Validation
        if not all([role, fullname, email, phone, password]):
            missing = []
            if not role: missing.append('role')
            if not fullname: missing.append('fullname')
            if not email: missing.append('email')
            if not phone: missing.append('phone')
            if not password: missing.append('password')
            return jsonify({'message': f'Missing fields: {", ".join(missing)}'}), 400

        if role not in ['patient', 'doctor', 'pharmacist', 'admin']:
            return jsonify({'message': f'Invalid role: {role}. Must be "patient", "doctor", "pharmacist", or "admin"'}), 400

        if not validate_email(email):
            return jsonify({'message': f'Invalid email format: {email}'}), 400

        if not validate_password(password):
            return jsonify({'message': 'Password must be at least 6 characters'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error - MySQL not running?'}), 500

        cursor = conn.cursor()

        try:
            # Check if email already exists
            cursor.execute('SELECT id, role FROM login WHERE email = %s', (email,))
            existing = cursor.fetchone()
            if existing:
                cursor.close()
                conn.close()
                return jsonify({'message': f'Email {email} is already registered'}), 409

            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

            # Build insert query based on role
            if role == 'doctor':
                specialization = data.get('specialization', '').strip()
                license_number = data.get('license_number', '').strip()
                experience_years = data.get('experience_years', 0)
                consultation_fee = data.get('consultation_fee', 500)

                if not all([specialization, license_number, experience_years, consultation_fee]):
                    missing_doc = []
                    if not specialization: missing_doc.append('specialization')
                    if not license_number: missing_doc.append('license_number')
                    if not experience_years: missing_doc.append('experience_years')
                    if not consultation_fee: missing_doc.append('consultation_fee')
                    return jsonify({'message': f'Missing doctor fields: {", ".join(missing_doc)}'}), 400

                cursor.execute('''
                    INSERT INTO login 
                    (full_name, email, phone, password, role, specialization, license_number, 
                     experience_years, consultation_fee)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fullname, email, phone, hashed_password, 'doctor', specialization, 
                      license_number, int(experience_years), int(consultation_fee)))
                
                print(f"OK - Doctor registered: {fullname} ({email}) - {specialization}")
                
            else:
                # Patient, Pharmacist, or Admin signup
                cursor.execute('''
                    INSERT INTO login (full_name, email, phone, password, role)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (fullname, email, phone, hashed_password, role))
                
                print(f"OK - {role.capitalize()} registered: {fullname} ({email})")

            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()

            return jsonify({
                'success': True,
                'message': f'{role.capitalize()} registered successfully!',
                'user_id': user_id,
                'role': role
            }), 201

        except mysql.connector.Error as db_err:
            cursor.close()
            conn.close()
            print(f"Database Error during signup: {db_err}")
            return jsonify({'message': f'Database error: {str(db_err)}'}), 500

    except Exception as e:
        print(f"Signup Error: {e}")
        return jsonify({'message': f'Error during registration: {str(e)}'}), 500


@app.route('/login', methods=['POST'])
def login():
    """Login user (Patient or Doctor)"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error'}), 500

        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute('''
                SELECT id, full_name, email, role, specialization, phone, password 
                FROM login WHERE email = %s
            ''', (email,))
            
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                print(f"Login failed: Email not found - {email}")
                return jsonify({'message': 'Invalid email or password'}), 401

            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                print(f"Login failed: Wrong password for {email}")
                return jsonify({'message': 'Invalid email or password'}), 401

            # Success
            role = user.get('role', 'patient')
            print(f"OK - Login successful: {user['full_name']} ({user['email']}) - Role: {role}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'full_name': user['full_name'],
                    'name': user['full_name'],  # For compatibility
                    'email': user['email'],
                    'role': role,
                    'phone': user['phone'],
                    'specialization': user.get('specialization', '')
                }
            }), 200

        except mysql.connector.Error as db_err:
            conn.close()
            print(f"Database error during login: {db_err}")
            return jsonify({'message': f'Database error: {str(db_err)}'}), 500

    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({'message': f'Error during login: {str(e)}'}), 500


@app.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    return jsonify({'message': 'Logged out successfully'}), 200


# ============ PASSWORD RECOVERY ENDPOINTS ============

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset for a user"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'message': 'Email is required'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error'}), 500

        cursor = conn.cursor(dictionary=True)

        try:
            # Check if user exists
            cursor.execute('SELECT id, full_name FROM login WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                # Don't reveal if email exists or not (security best practice)
                return jsonify({'message': 'If an account exists with this email, you will receive a password reset link'}), 200

            # Generate a temporary password (6-8 characters)
            temp_password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            hashed_temp = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

            # Update user's password with temporary one
            cursor.execute('UPDATE login SET password = %s WHERE id = %s', (hashed_temp, user['id']))
            conn.commit()
            
            cursor.close()
            conn.close()

            # In production, you would send this email. For now, return it in response.
            print(f"\nPASSWORD RESET REQUEST FOR: {email}")
            print(f"Temporary Password: {temp_password}")
            print(f"SHARE THIS ONLY WITH {user['full_name'].upper()}\n")

            return jsonify({
                'success': True,
                'message': 'Password reset successful. Check your email for the temporary password.',
                'temp_password': temp_password
            }), 200

        except mysql.connector.Error as db_err:
            cursor.close()
            conn.close()
            print(f"Database Error: {db_err}")
            return jsonify({'message': f'Database error: {str(db_err)}'}), 500

    except Exception as e:
        print(f"Forgot Password Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/reset-password', methods=['POST'])
def reset_password():
    """User resets password with temporary password"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        temp_password = data.get('temp_password', '')
        new_password = data.get('new_password', '')

        if not all([email, temp_password, new_password]):
            return jsonify({'message': 'Email, temporary password, and new password are required'}), 400

        if len(new_password) < 6:
            return jsonify({'message': 'New password must be at least 6 characters'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error'}), 500

        cursor = conn.cursor(dictionary=True)

        try:
            # Find user
            cursor.execute('SELECT id, password FROM login WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                return jsonify({'message': 'User not found'}), 404

            # Verify temporary password
            if not bcrypt.checkpw(temp_password.encode('utf-8'), user['password'].encode('utf-8')):
                cursor.close()
                conn.close()
                print(f"Invalid temporary password for {email}")
                return jsonify({'message': 'Invalid temporary password'}), 401

            # Hash new password
            hashed_new = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

            # Update password
            cursor.execute('UPDATE login SET password = %s WHERE id = %s', (hashed_new, user['id']))
            conn.commit()
            
            cursor.close()
            conn.close()

            print(f"OK - Password reset successful for {email}")
            return jsonify({
                'success': True,
                'message': 'Password has been successfully reset. You can now login with your new password.'
            }), 200

        except mysql.connector.Error as db_err:
            cursor.close()
            conn.close()
            print(f"Database Error: {db_err}")
            return jsonify({'message': f'Database error: {str(db_err)}'}), 500

    except Exception as e:
        print(f"Reset Password Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ PATIENT ENDPOINTS ============

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    """Patient books an appointment"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        reason_for_visit = data.get('reason_for_visit')
        consultation_type = data.get('consultation_type', 'in-person')

        # Validation
        if not all([patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit]):
            missing = []
            if not patient_id: missing.append('patient_id')
            if not doctor_id: missing.append('doctor_id')
            if not appointment_date: missing.append('appointment_date')
            if not appointment_time: missing.append('appointment_time')
            if not reason_for_visit: missing.append('reason_for_visit')
            
            return jsonify({
                'success': False, 
                'message': f'Required fields missing: {", ".join(missing)}'
            }), 400

        # Cleanup phone format if present
        if isinstance(appointment_time, str):
            appointment_time = appointment_time.strip()
        if isinstance(appointment_date, str):
            appointment_date = appointment_date.strip()

        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Database connection failed'
            }), 500

        cursor = conn.cursor()

        try:
            # Verify patient exists
            cursor.execute('SELECT id FROM login WHERE id = %s AND role = "patient"', (patient_id,))
            if not cursor.fetchone():
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Patient not found'
                }), 404

            # Verify doctor exists
            cursor.execute('SELECT id FROM login WHERE id = %s AND role = "doctor"', (doctor_id,))
            if not cursor.fetchone():
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Doctor not found'
                }), 404

            # Insert appointment
            cursor.execute('''
                INSERT INTO appointments 
                (patient_id, doctor_id, appointment_date, appointment_time, 
                 reason_for_visit, consultation_type, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'scheduled')
            ''', (int(patient_id), int(doctor_id), appointment_date, appointment_time, 
                  reason_for_visit, consultation_type))

            conn.commit()
            appointment_id = cursor.lastrowid
            
            print(f"OK - Appointment booked: Patient {patient_id} with Doctor {doctor_id} on {appointment_date} at {appointment_time}")
            
            cursor.close()
            conn.close()

            return jsonify({
                'success': True, 
                'message': 'Appointment booked successfully', 
                'appointment_id': appointment_id
            }), 201

        except mysql.connector.Error as db_err:
            conn.close()
            print(f"Database Error in book_appointment: {db_err}")
            return jsonify({
                'success': False,
                'message': f'Database error: {str(db_err)}'
            }), 500

    except Exception as e:
        print(f"Appointment Error: {e}")
        return jsonify({
            'success': False, 
            'message': f'Error booking appointment: {str(e)}'
        }), 500


@app.route('/get-patient-appointments/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    """Get all appointments for a patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT a.*, l.full_name as doctor_name, l.specialization
            FROM appointments a
            JOIN login l ON a.doctor_id = l.id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_date DESC
        ''', (patient_id,))

        appointments = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert timedelta and date objects to strings
        def serialize_data(data_list):
            result = []
            if data_list:
                for item in data_list:
                    if item:
                        for key, value in item.items():
                            if hasattr(value, 'total_seconds'):  # timedelta object
                                item[key] = str(value)
                            elif value and isinstance(value, (date, datetime)):
                                item[key] = str(value)
                    result.append(item)
            return result

        appointments = serialize_data(appointments)

        return jsonify({'appointments': appointments}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/delete-appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Delete/cancel an appointment"""
    try:
        data = request.get_json() or {}
        patient_id = data.get('patient_id')

        if not patient_id:
            return jsonify({'message': 'Patient ID is required'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Verify the appointment belongs to this patient
        cursor.execute('''
            SELECT patient_id FROM appointments WHERE id = %s
        ''', (appointment_id,))
        
        appointment = cursor.fetchone()
        if not appointment:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Appointment not found'}), 404

        if appointment['patient_id'] != patient_id:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Unauthorized'}), 403

        # Delete the appointment
        cursor.execute('DELETE FROM appointments WHERE id = %s', (appointment_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Appointment deleted successfully'}), 200

    except Exception as e:
        print(f"Error deleting appointment: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/get-medical-history/<int:patient_id>', methods=['GET'])
def get_medical_history(patient_id):
    """Get medical history for a patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Get illness history
        cursor.execute('''
            SELECT * FROM patient_illness_history
            WHERE patient_id = %s
            ORDER BY onset_date DESC
        ''', (patient_id,))

        illness_history = cursor.fetchall()

        # Get medical records with doctor info
        cursor.execute('''
            SELECT 
                mr.*,
                d.full_name as doctor_name
            FROM patient_medical_records mr
            LEFT JOIN login d ON mr.doctor_id = d.id
            WHERE mr.patient_id = %s
            ORDER BY mr.record_date DESC
        ''', (patient_id,))

        medical_records = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'illness_history': illness_history,
            'records': medical_records
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/get-prescriptions/<int:patient_id>', methods=['GET'])
def get_prescriptions(patient_id):
    """Get prescriptions for a patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT p.*, l.full_name as doctor_name
            FROM prescriptions p
            JOIN login l ON p.doctor_id = l.id
            WHERE p.patient_id = %s AND p.status = 'active'
            ORDER BY p.prescription_date DESC
        ''', (patient_id,))

        prescriptions = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'prescriptions': prescriptions}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500

# ============ DOCTOR ENDPOINTS ============

@app.route('/get-doctor-patients/<int:doctor_id>', methods=['GET'])
def get_doctor_patients(doctor_id):
    """Get all patients for a doctor"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT DISTINCT p.id, p.full_name, p.email, p.phone, p.date_of_birth
            FROM login p
            JOIN appointments a ON p.id = a.patient_id
            WHERE a.doctor_id = %s AND p.role = 'patient'
            ORDER BY p.full_name
        ''', (doctor_id,))

        patients = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'patients': patients}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/add-consultation', methods=['POST'])
def add_consultation():
    """Doctor adds consultation and prescription"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        symptoms = data.get('symptoms')
        diagnosis = data.get('diagnosis')
        comments = data.get('comments', '')
        medicine_name = data.get('medicine_name')
        dosage = data.get('dosage')
        frequency = data.get('frequency')
        duration = data.get('duration')
        instructions = data.get('instructions')

        if not all([patient_id, doctor_id, symptoms, diagnosis, medicine_name]):
            return jsonify({'message': 'All required fields missing'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor()

        # Get latest appointment
        cursor.execute('''
            SELECT id FROM appointments 
            WHERE patient_id = %s AND doctor_id = %s
            ORDER BY appointment_date DESC LIMIT 1
        ''', (patient_id, doctor_id))
        appointment = cursor.fetchone()
        appointment_id = appointment[0] if appointment else None

        # Insert medical record with comments
        cursor.execute('''
            INSERT INTO patient_medical_records 
            (patient_id, doctor_id, appointment_id, symptoms, diagnosis, comments)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (patient_id, doctor_id, appointment_id, symptoms, diagnosis, comments))

        record_id = cursor.lastrowid

        # If there is no appointment, create a lightweight placeholder appointment
        # so that prescriptions (which require appointment_id NOT NULL) can be created.
        if not appointment_id:
            try:
                cursor.execute('''
                    INSERT INTO appointments 
                    (patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, consultation_type, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    patient_id,
                    doctor_id,
                    datetime.now().strftime('%Y-%m-%d'),
                    datetime.now().strftime('%H:%M:%S'),
                    'Prescription (auto-created)',
                    'in-person',
                    'completed'
                ))
                # assign new appointment id for prescription foreign key
                appointment_id = cursor.lastrowid
                print(f'DEBUG: Auto-created appointment id {appointment_id} for prescription')
            except Exception as e:
                print('DEBUG: failed to auto-create appointment for prescription:', e)

        # Insert prescription
        prescription_date = datetime.now().strftime('%Y-%m-%d')
        expiry_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        cursor.execute('''
            INSERT INTO prescriptions
            (appointment_id, patient_id, doctor_id, medicine_name, dosage, 
             frequency, duration, instructions, prescription_date, expiry_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')
        ''', (appointment_id, patient_id, doctor_id, medicine_name, dosage,
              frequency, duration, instructions, prescription_date, expiry_date))

        # capture prescription id for notification
        prescription_id = cursor.lastrowid

        # Attempt to decrement medicine stock by requested quantity (supports spanning multiple batches)
        updated_medicines = []
        remaining = int(data.get('quantity', 1) or 1)
        try:
            # If frontend provided a specific medicine_id, try decrementing that row first
            med_id_provided = data.get('medicine_id') or data.get('medicineId')
            if med_id_provided:
                try:
                    mid = int(med_id_provided)
                    cursor.execute('SELECT id, quantity, batch_no, expiry_date, name FROM medicines WHERE id = %s FOR UPDATE', (mid,))
                    row = cursor.fetchone()
                    print('DEBUG: medicine_id lookup ->', row)
                    if row and int(row[1]) > 0:
                        med_qty = int(row[1])
                        take = med_qty if med_qty <= remaining else remaining
                        new_qty = med_qty - take
                        cursor.execute('UPDATE medicines SET quantity = %s WHERE id = %s', (new_qty, mid))
                        updated_medicines.append({'id': mid, 'name': row[4] if len(row) > 4 else medicine_name, 'quantity': new_qty, 'batch_no': row[2] if len(row) > 2 else None, 'expiry_date': str(row[3]) if len(row) > 3 else None})
                        remaining -= take
                except Exception as ex:
                    print('DEBUG: medicine_id decrement error:', ex)

            # If still remaining, fall back to name-based batches (earliest expiry first)
            while remaining > 0:
                cursor.execute('''
                    SELECT id, quantity, batch_no, expiry_date FROM medicines
                    WHERE name = %s AND quantity > 0
                    ORDER BY expiry_date ASC
                    LIMIT 1 FOR UPDATE
                ''', (medicine_name,))
                med_row = cursor.fetchone()
                print('DEBUG: medicine lookup result for', medicine_name, '->', med_row)
                if not med_row:
                    print('DEBUG: no medicine row found to decrement')
                    break
                med_id = med_row[0]
                med_qty = int(med_row[1])
                take = med_qty if med_qty <= remaining else remaining
                new_qty = med_qty - take
                print(f"DEBUG: decrementing med id={med_id} by {take} (was {med_qty}, now {new_qty})")
                cursor.execute('UPDATE medicines SET quantity = %s WHERE id = %s', (new_qty, med_id))
                updated_medicines.append({'id': med_id, 'name': medicine_name, 'quantity': new_qty, 'batch_no': med_row[2] if len(med_row) > 2 else None, 'expiry_date': str(med_row[3]) if len(med_row) > 3 else None})
                remaining -= take
        except Exception as ex:
            print(f"Error updating medicine stock: {ex}")

        conn.commit()
        cursor.close()
        conn.close()

        resp = {'success': True, 'message': 'Consultation and prescription saved', 'record_id': record_id}
        if updated_medicines:
            resp['updated_medicines'] = updated_medicines
            # Notify connected clients and persist notifications
            try:
                for m in updated_medicines:
                    notify_clients({'type': 'medicine_stock_update', 'medicine': m})
            except Exception as e:
                print('Warning: notify_clients failed:', e)
        # Notify patient about new prescription (so patient portal can refresh)
        try:
            pres_event = {
                'type': 'prescription_created',
                'patient_id': patient_id,
                'prescription': {
                    'id': prescription_id,
                    'medicine_name': medicine_name,
                    'dosage': dosage,
                    'frequency': frequency,
                    'duration': duration,
                    'prescription_date': prescription_date
                },
                'target_role': 'patient'
            }
            notify_clients(pres_event)
        except Exception as e:
            print('Warning: notify_clients (prescription) failed:', e)
        if remaining > 0:
            resp['warning'] = f'Only some stock could be decremented; {remaining} unit(s) not found in inventory.'

        return jsonify(resp), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/get-doctor-appointments/<int:doctor_id>', methods=['GET'])
def get_doctor_appointments(doctor_id):
    """Get appointments for a doctor"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Get today's appointments
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT a.*, p.full_name as patient_name, p.email as patient_email
            FROM appointments a
            JOIN login p ON a.patient_id = p.id
            WHERE a.doctor_id = %s AND a.appointment_date = %s
            ORDER BY a.appointment_time
        ''', (doctor_id, today))

        today_appointments = cursor.fetchall()

        # Get all upcoming appointments
        cursor.execute('''
            SELECT a.*, p.full_name as patient_name
            FROM appointments a
            JOIN login p ON a.patient_id = p.id
            WHERE a.doctor_id = %s AND a.appointment_date >= %s AND a.status = 'scheduled'
            ORDER BY a.appointment_date, a.appointment_time
            LIMIT 20
        ''', (doctor_id, today))

        upcoming_appointments = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert timedelta objects to strings
        def serialize_appointments(appointments):
            result = []
            for appt in appointments:
                if appt:
                    for key, value in appt.items():
                        if hasattr(value, 'total_seconds'):  # timedelta object
                            appt[key] = str(value)
                        elif value and isinstance(value, (date, datetime)):
                            appt[key] = str(value)
                result.append(appt)
            return result

        today_appointments = serialize_appointments(today_appointments)
        upcoming_appointments = serialize_appointments(upcoming_appointments)

        return jsonify({
            'today': today_appointments,
            'upcoming': upcoming_appointments
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/get-patient-details/<int:patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    """Get detailed information about a patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Get patient basic info
        cursor.execute('''
            SELECT id, full_name, email, phone, date_of_birth, gender, address, city
            FROM login WHERE id = %s AND role = 'patient'
        ''', (patient_id,))
        patient_info = cursor.fetchone()

        if not patient_info:
            return jsonify({'message': 'Patient not found'}), 404

        # Get vital signs from latest medical record
        cursor.execute('''
            SELECT blood_pressure, temperature, heart_rate, weight, height, bmi
            FROM patient_medical_records
            WHERE patient_id = %s
            ORDER BY record_date DESC LIMIT 1
        ''', (patient_id,))
        vitals = cursor.fetchone()

        # Get allergies
        cursor.execute('''
            SELECT allergies, chronic_conditions
            FROM patient_medical_records
            WHERE patient_id = %s
            ORDER BY record_date DESC LIMIT 1
        ''', (patient_id,))
        health_info = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            'patient_info': patient_info,
            'vitals': vitals,
            'health_info': health_info
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500

# ============ GENERAL ENDPOINTS ============

@app.route('/get-doctors', methods=['GET'])
def get_doctors():
    """Get list of all doctors"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        # Detect which columns exist in `login` to avoid SQL errors on minimal schemas
        info_cursor = conn.cursor()
        info_cursor.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME='login'",
            (DB_CONFIG['database'],)
        )
        cols = [row[0].lower() for row in info_cursor.fetchall()]
        info_cursor.close()

        has_role = 'role' in cols
        has_spec = 'specialization' in cols
        has_exp = 'experience_years' in cols
        has_fee = 'consultation_fee' in cols

        # Build a safe SELECT that provides fallback empty values when columns missing
        select_fields = ['id', 'full_name']
        select_fields.append('specialization' if has_spec else "'' AS specialization")
        select_fields.append('experience_years' if has_exp else '0 AS experience_years')
        select_fields.append('consultation_fee' if has_fee else '0 AS consultation_fee')

        where_clause = "WHERE role = 'doctor'" if has_role else ''

        query = f"SELECT {', '.join(select_fields)} FROM login {where_clause} ORDER BY full_name"

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        doctors = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'doctors': doctors}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500


# ============ ENHANCED FEATURES (NEW) ============

@app.route('/api/lab-result', methods=['POST'])
def api_add_lab_result():
    """Add lab result for patient"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        test_name = data.get('test_name')
        result_value = data.get('result_value')
        result_unit = data.get('result_unit', '')
        reference_range = data.get('reference_range', '')
        status = data.get('status', 'normal')
        notes = data.get('notes', '')
        test_date = data.get('test_date', datetime.now().strftime('%Y-%m-%d'))

        if not all([patient_id, doctor_id, test_name, result_value]):
            return jsonify({'message': 'Missing required fields'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor()
        cursor.execute("""INSERT INTO lab_results (patient_id, doctor_id, test_name, test_date, result_value, result_unit, reference_range, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (patient_id, doctor_id, test_name, test_date, result_value, result_unit, reference_range, status, notes))
        conn.commit()
        result_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"OK - Lab result added for patient {patient_id}")
        return jsonify({'message': 'Lab result added', 'result_id': result_id}), 201
    except Exception as e:
        print(f"Error adding lab result: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/lab-results/<int:patient_id>', methods=['GET'])
def api_get_lab_results(patient_id):
    """Get lab results for patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lab_results WHERE patient_id = %s ORDER BY test_date DESC", (patient_id,))
        results = cursor.fetchall()
        # Convert date objects to strings
        for r in results:
            if r['test_date']:
                r['test_date'] = str(r['test_date'])
            if 'created_at' in r and r['created_at']:
                r['created_at'] = str(r['created_at'])
        cursor.close()
        conn.close()
        return jsonify({'lab_results': results}), 200
    except Exception as e:
        print(f"Error getting lab results: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/alert', methods=['POST'])
def api_add_alert():
    """Add patient alert"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id', 0)
        alert_message = data.get('alert_message')
        severity = data.get('severity', 'low')
        alert_type = data.get('alert_type', '')

        if not all([patient_id, alert_message]):
            return jsonify({'message': 'Missing required fields'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO patient_alerts (patient_id, alert_title, alert_message, severity, alert_type, created_by, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())""", (patient_id, alert_type, alert_message, severity, alert_type, doctor_id))
        conn.commit()
        alert_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"OK - Alert created for patient {patient_id}")
        return jsonify({'message': 'Alert created', 'alert_id': alert_id}), 201
    except Exception as e:
        print(f"Error creating alert: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/alerts/<int:patient_id>', methods=['GET'])
def api_get_alerts(patient_id):
    """Get alerts for patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patient_alerts WHERE patient_id = %s ORDER BY created_at DESC", (patient_id,))
        alerts = cursor.fetchall()
        # Convert datetime objects to strings
        for a in alerts:
            if 'created_at' in a and a['created_at']:
                a['created_at'] = str(a['created_at'])
        cursor.close()
        conn.close()
        return jsonify({'alerts': alerts}), 200
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/alert/<int:alert_id>/read', methods=['POST'])
def api_mark_alert_read(alert_id):
    """Mark alert as read"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        cursor.execute("UPDATE patient_alerts SET is_read = 1 WHERE id = %s", (alert_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Alert marked read'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/followup', methods=['POST'])
def api_schedule_followup():
    """Schedule follow-up appointment"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        followup_date = data.get('followup_date')
        followup_time = data.get('followup_time')
        reason = data.get('reason', '')

        if not all([patient_id, doctor_id, followup_date, followup_time]):
            return jsonify({'message': 'Missing required fields'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO follow_ups (patient_id, doctor_id, follow_up_date, follow_up_time, reason, scheduled_by, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())""", (patient_id, doctor_id, followup_date, followup_time, reason, doctor_id))
        conn.commit()
        followup_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"OK - Follow-up scheduled for patient {patient_id}")
        return jsonify({'message': 'Follow-up scheduled', 'followup_id': followup_id}), 201
    except Exception as e:
        print(f"Error scheduling follow-up: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/followups/<int:patient_id>', methods=['GET'])
def api_get_followups(patient_id):
    """Get follow-ups for patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM follow_ups WHERE patient_id = %s ORDER BY follow_up_date ASC", (patient_id,))
        followups = cursor.fetchall()
        # Convert date/time objects to strings for JSON
        for f in followups:
            if f['follow_up_date']:
                f['follow_up_date'] = str(f['follow_up_date'])
            if f['follow_up_time']:
                f['follow_up_time'] = str(f['follow_up_time'])
        cursor.close()
        conn.close()
        return jsonify({'followups': followups}), 200
    except Exception as e:
        print(f"Error getting followups: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/appointment/<int:appointment_id>/reschedule', methods=['POST'])
def api_reschedule_appointment(appointment_id):
    """Reschedule appointment"""
    try:
        data = request.json
        new_date = data.get('new_date')
        new_time = data.get('new_time')
        reason = data.get('reason', '')

        if not all([new_date, new_time]):
            return jsonify({'message': 'Missing required fields'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
        original = cursor.fetchone()
        
        if not original:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Appointment not found'}), 404

        cursor.close()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO appointment_reschedules (original_appointment_id, patient_id, old_date, old_time, new_date, new_time, reason, rescheduled_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (appointment_id, original['patient_id'], original['appointment_date'], original['appointment_time'], new_date, new_time, reason, original['patient_id']))
        cursor.execute("UPDATE appointments SET appointment_date = %s, appointment_time = %s WHERE id = %s", (new_date, new_time, appointment_id))
        conn.commit()
        reschedule_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"OK - Appointment {appointment_id} rescheduled")
        return jsonify({'message': 'Appointment rescheduled', 'reschedule_id': reschedule_id}), 200
    except Exception as e:
        print(f"Error rescheduling: {e}")
        return jsonify({'message': str(e)}), 500


# ============ PHARMACY / MEDICINES ENDPOINTS ============
def ensure_medicines_table_exists():
    """Create medicines table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if not conn:
            print("Cannot ensure medicines table: DB connection failed")
            return
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                sku VARCHAR(100) DEFAULT '',
                manufacturer VARCHAR(255) DEFAULT '',
                batch_no VARCHAR(100) DEFAULT '',
                expiry_date DATE DEFAULT NULL,
                quantity INT DEFAULT 0,
                unit_price DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("OK - medicines table ensured")
    except Exception as e:
        print(f"Error creating medicines table: {e}")


# Simple in-memory SSE client registry
_sse_clients = []

def notify_clients(event):
    """Push a JSON-serializable event to all connected SSE clients"""
    # Use a copy to avoid mutation during iteration
    # Persist notification to DB (best-effort)
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            etype = event.get('type') if isinstance(event, dict) else str(event)
            payload = json.dumps(event, default=str)
            # Prefer explicit target_role in the event if provided, otherwise decide heuristically
            target = None
            if isinstance(event, dict) and event.get('target_role'):
                target = event.get('target_role')
            else:
                if etype == 'medicine_added':
                    target = 'admin'
                elif etype == 'restock_update':
                    # restock updates are relevant to pharmacists
                    target = 'pharmacist'
            cursor.execute('INSERT INTO notifications (event_type, payload, target_role) VALUES (%s,%s,%s)', (etype, payload, target))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print('Warning: could not persist notification:', e)

    for q in list(_sse_clients):
        try:
            q.put(event, block=False)
        except Exception:
            # ignore if queue full or closed
            pass


@app.route('/stream')
def sse_stream():
    """Server-Sent Events endpoint for real-time notifications"""
    def gen(q):
        try:
            # Send an initial comment/heartbeat so clients don't time out
            yield ': connected\n\n'
            while True:
                try:
                    # Wait for an event, but periodically send heartbeats so proxies/clients stay alive
                    event = q.get(timeout=10)
                    data = json.dumps(event, default=str)
                    yield f"data: {data}\n\n"
                except queue.Empty:
                    # heartbeat comment (ignored by EventSource) to keep connection active
                    yield ': heartbeat\n\n'
                    continue
        except GeneratorExit:
            return
        finally:
            # Ensure client queue is removed on disconnect
            try:
                _sse_clients.remove(q)
            except Exception:
                pass

    q = queue.Queue()
    _sse_clients.append(q)
    return Response(stream_with_context(gen(q)), mimetype='text/event-stream')


@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    """Get recent notifications for a role/user"""
    try:
        actor_id = request.args.get('actor_id')
        role = request.args.get('role')
        limit = int(request.args.get('limit') or 50)

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)

        # Basic role filtering
        if role:
            cursor.execute('SELECT * FROM notifications WHERE target_role = %s ORDER BY created_at DESC LIMIT %s', (role, limit))
        else:
            cursor.execute('SELECT * FROM notifications ORDER BY created_at DESC LIMIT %s', (limit,))

        notifs = cursor.fetchall()
        cursor.close()
        conn.close()

        # Parse payload JSON
        for n in notifs:
            try:
                n['payload'] = json.loads(n['payload']) if n.get('payload') else None
            except Exception:
                n['payload'] = n.get('payload')

        return jsonify({'notifications': notifs}), 200
    except Exception as e:
        print('Error getting notifications:', e)
        return jsonify({'message': str(e)}), 500


@app.route('/api/notifications/<int:notif_id>/mark-seen', methods=['PUT'])
def api_mark_notification_seen(notif_id):
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = data.get('role')

        if not role:
            return jsonify({'message': 'Role required to mark notifications seen'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()

        if role == 'admin':
            cursor.execute('UPDATE notifications SET is_seen_admin = 1 WHERE id = %s', (notif_id,))
        elif role == 'pharmacist':
            cursor.execute('UPDATE notifications SET is_seen_pharmacist = 1 WHERE id = %s', (notif_id,))
        else:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Unknown role'}), 400

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Marked seen'}), 200
    except Exception as e:
        print('Error marking notification seen:', e)
        return jsonify({'message': str(e)}), 500


def _get_user_role(user_id):
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, role FROM login WHERE id = %s', (user_id,))
        u = cursor.fetchone()
        cursor.close()
        conn.close()
        return u['role'] if u else None
    except Exception:
        return None


@app.route('/api/medicines', methods=['GET'])
def api_get_medicines():
    """List medicines (optional low_stock filter)"""
    try:
        threshold = request.args.get('low_stock')
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        if threshold:
            try:
                t = int(threshold)
            except:
                t = 10
            cursor.execute('SELECT * FROM medicines WHERE quantity <= %s ORDER BY name', (t,))
        else:
            cursor.execute('SELECT * FROM medicines ORDER BY name')
        meds = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert dates to strings
        for m in meds:
            if m.get('expiry_date'):
                m['expiry_date'] = str(m['expiry_date'])
        return jsonify({'medicines': meds}), 200
    except Exception as e:
        print(f"Error getting medicines: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/medicines', methods=['POST'])
def api_add_medicine():
    """Add a new medicine (pharmacist or admin only)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role not in ['pharmacist', 'admin']:
            return jsonify({'message': 'Only pharmacist or admin can add medicines'}), 403

        name = data.get('name', '').strip()
        sku = data.get('sku', '').strip()
        manufacturer = data.get('manufacturer', '').strip()
        batch_no = data.get('batch_no', '').strip()
        expiry_date = data.get('expiry_date') or None

        # Validate required fields
        if not name:
            return jsonify({'message': 'Medicine name is required'}), 400

        # Validate quantity field exists and is a valid number
        if 'quantity' not in data or data.get('quantity') is None:
            return jsonify({'message': 'Quantity is required'}), 400
        
        try:
            quantity = int(data.get('quantity'))
            if quantity < 0:
                return jsonify({'message': 'Quantity cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'message': 'Quantity must be a valid number'}), 400

        # Validate unit_price field exists and is a valid number
        if 'unit_price' not in data or data.get('unit_price') is None:
            return jsonify({'message': 'Unit price is required'}), 400
        
        try:
            unit_price = float(data.get('unit_price'))
            if unit_price < 0:
                return jsonify({'message': 'Unit price cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'message': 'Unit price must be a valid number'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medicines (name, sku, manufacturer, batch_no, expiry_date, quantity, unit_price)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''', (name, sku, manufacturer, batch_no, expiry_date, quantity, unit_price))
        conn.commit()
        med_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"OK - Medicine added: {name} (id={med_id}) by user {actor_id}")
        # Notify SSE clients about the new medicine
        try:
            notify_clients({
                'type': 'medicine_added',
                'medicine': {
                    'id': med_id,
                    'name': name,
                    'quantity': quantity,
                    'unit_price': unit_price
                },
                'added_by': actor_id
            })
        except Exception:
            pass

        return jsonify({'message': 'Medicine added', 'medicine_id': med_id}), 201
    except Exception as e:
        print(f"Error adding medicine: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/medicines/<int:med_id>', methods=['PUT'])
def api_update_medicine(med_id):
    """Update medicine record (pharmacist or admin)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role not in ['pharmacist', 'admin']:
            return jsonify({'message': 'Only pharmacist or admin can update medicines'}), 403

        fields = []
        values = []
        for key in ['name','sku','manufacturer','batch_no','expiry_date','quantity','unit_price']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])

        if not fields:
            return jsonify({'message': 'No fields to update'}), 400

        values.append(med_id)
        query = 'UPDATE medicines SET ' + ', '.join(fields) + ' WHERE id = %s'

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"OK - Medicine {med_id} updated by user {actor_id}")
        return jsonify({'message': 'Medicine updated'}), 200
    except Exception as e:
        print(f"Error updating medicine: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/medicines/<int:med_id>', methods=['DELETE'])
def api_delete_medicine(med_id):
    """Delete medicine (admin only)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        # Allow admin or pharmacist to delete medicines from their portal
        if role not in ['admin', 'pharmacist']:
            return jsonify({'message': 'Only admin or pharmacist can delete medicines'}), 403

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500

        cursor = conn.cursor()
        cursor.execute('DELETE FROM medicines WHERE id = %s', (med_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"OK - Medicine {med_id} deleted by admin {actor_id}")
        return jsonify({'message': 'Medicine deleted'}), 200
    except Exception as e:
        print(f"Error deleting medicine: {e}")
        return jsonify({'message': str(e)}), 500


# ============ ADMIN MANAGEMENT ENDPOINTS ============

@app.route('/api/admin/users', methods=['GET'])
def api_get_all_users():
    """List all users (admin only)"""
    try:
        actor_id = request.args.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can list users'}), 403

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, full_name, email, phone, role FROM login ORDER BY full_name')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'users': users}), 200
    except Exception as e:
        print(f"Error getting users: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/user/<int:user_id>/role', methods=['PUT'])
def api_update_user_role(user_id):
    """Update user role (admin only)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can update roles'}), 403

        new_role = data.get('role', '').strip().lower()
        if new_role not in ['patient', 'doctor', 'pharmacist', 'admin']:
            return jsonify({'message': f'Invalid role: {new_role}'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        cursor.execute('UPDATE login SET role = %s WHERE id = %s', (new_role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"OK - User {user_id} role updated to {new_role} by admin {actor_id}")
        return jsonify({'message': f'User role updated to {new_role}'}), 200
    except Exception as e:
        print(f"Error updating user role: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/user/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can delete users'}), 403

        if user_id == actor_id:
            return jsonify({'message': 'Cannot delete your own account'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        cursor.execute('DELETE FROM login WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"OK - User {user_id} deleted by admin {actor_id}")
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/settings', methods=['GET'])
def api_get_hospital_settings():
    """Get hospital settings (any authenticated user)"""
    try:
        # Simple in-memory settings for now; could be stored in DB table
        settings = {
            'hospital_name': 'Hospital and community Pharmacy management',
            'address': 'Central Medical Plaza',
            'phone': '+1-800-HEALTH-1',
            'email': 'admin@hospital.local',
            'operating_hours': '24/7',
            'max_patients_per_day': 150,
            'average_consultation_time': 30
        }
        return jsonify({'settings': settings}), 200
    except Exception as e:
        print(f"Error getting settings: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/settings', methods=['PUT'])
def api_update_hospital_settings():
    """Update hospital settings (admin only)"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can update settings'}), 403

        # In production, save to DB table `hospital_settings`
        # For now, just echo back validation
        allowed_keys = ['address', 'phone', 'email', 'operating_hours', 'max_patients_per_day', 'average_consultation_time']
        updated = {}
        for key in allowed_keys:
            if key in data:
                updated[key] = data[key]

        print(f"OK - Hospital settings updated by admin {actor_id}: {updated}")
        return jsonify({'message': 'Settings updated', 'updated': updated}), 200
    except Exception as e:
        print(f"Error updating settings: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Hospital and community Pharmacy management'}), 200

# ============ STATIC FILE SERVING ============
@app.route('/')
def root():
    """Serve hospital_landing.html as root"""
    file_path = os.path.join(BASE_DIR, 'hospital_landing.html')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    return 'Hospital Landing Page - Files not found', 404

@app.route('/<filename>')
def serve_file(filename):
    """Serve HTML and static files"""
    file_path = os.path.join(BASE_DIR, filename)
    
    # Security: Prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(BASE_DIR)):
        return 'Access Denied', 403
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Set appropriate content type
        if filename.endswith('.html'):
            return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        elif filename.endswith('.css'):
            return content, 200, {'Content-Type': 'text/css; charset=utf-8'}
        elif filename.endswith('.js'):
            return content, 200, {'Content-Type': 'application/javascript; charset=utf-8'}
        else:
            return content, 200
    
    return f'File not found: {filename}', 404

def ensure_restock_table_exists():
    """Create restock requests table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if not conn:
            print("Cannot ensure restock table: DB connection failed")
            return
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restock_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                medicine_id INT NOT NULL,
                medicine_name VARCHAR(255) NOT NULL,
                requested_by INT NOT NULL,
                requested_quantity INT NOT NULL,
                reason TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                admin_notes TEXT,
                approved_by INT,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP NULL,
                FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE,
                FOREIGN KEY (requested_by) REFERENCES login(id) ON DELETE CASCADE,
                FOREIGN KEY (approved_by) REFERENCES login(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("OK - restock_requests table ensured")
    except Exception as e:
        print(f"Error creating restock table: {e}")


def ensure_notifications_table_exists():
    """Create notifications table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if not conn:
            print("Cannot ensure notifications table: DB connection failed")
            return
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_type VARCHAR(100) NOT NULL,
                payload TEXT,
                target_role VARCHAR(100),
                is_seen_admin TINYINT DEFAULT 0,
                is_seen_pharmacist TINYINT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("OK - notifications table ensured")
    except Exception as e:
        print(f"Error creating notifications table: {e}")


# ============ PHARMACIST-ADMIN RESTOCK SYSTEM ============

@app.route('/api/pharmacist/inventory', methods=['GET'])
def api_pharmacist_inventory():
    """Get inventory for pharmacist portal"""
    try:
        actor_id = request.args.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'pharmacist':
            return jsonify({'message': 'Only pharmacist can access this'}), 403

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        
        # Get all medicines with their restock request status
        cursor.execute('''
            SELECT m.*, 
                   COUNT(CASE WHEN r.status='pending' THEN 1 END) as pending_requests
            FROM medicines m
            LEFT JOIN restock_requests r ON m.id = r.medicine_id
            GROUP BY m.id
            ORDER BY m.quantity ASC
        ''')
        
        medicines = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert dates to strings
        for m in medicines:
            if m.get('expiry_date'):
                m['expiry_date'] = str(m['expiry_date'])
            if m.get('created_at'):
                m['created_at'] = str(m['created_at'])
        
        return jsonify({'medicines': medicines}), 200
    except Exception as e:
        print(f"Error getting pharmacist inventory: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/restock-request', methods=['POST'])
def api_create_restock_request():
    """Pharmacist creates a restock request"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'pharmacist':
            return jsonify({'message': 'Only pharmacist can request restock'}), 403

        medicine_id = data.get('medicine_id')
        medicine_name = data.get('medicine_name', '').strip()
        requested_quantity = data.get('requested_quantity')
        reason = data.get('reason', 'Low stock').strip()

        if not all([medicine_id, medicine_name, requested_quantity]):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            requested_quantity = int(requested_quantity)
        except:
            return jsonify({'message': 'Quantity must be a number'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO restock_requests 
            (medicine_id, medicine_name, requested_by, requested_quantity, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        ''', (medicine_id, medicine_name, actor_id, requested_quantity, reason))
        
        conn.commit()
        request_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"OK - Restock request created: {medicine_name} x{requested_quantity} by pharmacist {actor_id}")
        return jsonify({'success': True, 'message': 'Restock request submitted', 'request_id': request_id}), 201
    except Exception as e:
        print(f"Error creating restock request: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/pharmacist/restock-requests', methods=['GET'])
def api_get_pharmacist_restock_requests():
    """Pharmacist views their own submitted restock requests"""
    try:
        actor_id = request.args.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'pharmacist':
            return jsonify({'message': 'Only pharmacist can view their requests'}), 403

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT id, medicine_name, requested_quantity, reason, status, admin_notes, requested_at, approved_at
            FROM restock_requests 
            WHERE requested_by = %s
            ORDER BY requested_at DESC
        ''', (actor_id,))
        
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Format dates
        for req in requests:
            if req.get('requested_at'):
                req['requested_at'] = str(req['requested_at'])
            if req.get('approved_at'):
                req['approved_at'] = str(req['approved_at'])
        
        return jsonify({'requests': requests}), 200
    except Exception as e:
        print(f"Error getting pharmacist requests: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/restock-requests', methods=['GET'])
def api_get_restock_requests():
    """Admin views all restock requests"""
    try:
        actor_id = request.args.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can view restock requests'}), 403

        status_filter = request.args.get('status', '')  # pending, approved, rejected, all
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        
        if status_filter and status_filter != 'all':
            cursor.execute('''
                SELECT r.*, p.full_name as pharmacist_name, a.full_name as admin_name
                FROM restock_requests r
                JOIN login p ON r.requested_by = p.id
                LEFT JOIN login a ON r.approved_by = a.id
                WHERE r.status = %s
                ORDER BY r.requested_at DESC
            ''', (status_filter,))
        else:
            cursor.execute('''
                SELECT r.*, p.full_name as pharmacist_name, a.full_name as admin_name
                FROM restock_requests r
                JOIN login p ON r.requested_by = p.id
                LEFT JOIN login a ON r.approved_by = a.id
                ORDER BY r.requested_at DESC
            ''')
        
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert timestamps to strings
        for req in requests:
            if req.get('requested_at'):
                req['requested_at'] = str(req['requested_at'])
            if req.get('approved_at'):
                req['approved_at'] = str(req['approved_at'])
        
        return jsonify({'requests': requests}), 200
    except Exception as e:
        print(f"Error getting restock requests: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/restock-request/<int:request_id>/approve', methods=['PUT'])
def api_approve_restock_request(request_id):
    """Admin approves restock request and updates inventory"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can approve requests'}), 403

        admin_notes = data.get('admin_notes', '').strip()

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor(dictionary=True)
        
        # Get the request
        cursor.execute('SELECT * FROM restock_requests WHERE id = %s', (request_id,))
        request_record = cursor.fetchone()
        
        if not request_record:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Request not found'}), 404

        # Update request status
        cursor.execute('''
            UPDATE restock_requests 
            SET status = 'approved', approved_by = %s, approved_at = NOW(), admin_notes = %s
            WHERE id = %s
        ''', (actor_id, admin_notes, request_id))

        # Get old quantity before update
        cursor.execute('SELECT quantity FROM medicines WHERE id = %s', (request_record['medicine_id'],))
        old_med = cursor.fetchone()
        old_quantity = old_med['quantity'] if old_med else 0

        # Update medicine quantity
        new_quantity = old_quantity + request_record['requested_quantity']
        cursor.execute('''
            UPDATE medicines 
            SET quantity = %s 
            WHERE id = %s
        ''', (new_quantity, request_record['medicine_id']))

        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"OK - Restock request {request_id} approved by admin {actor_id}: +{request_record['requested_quantity']} {request_record['medicine_name']}")
        # Notify SSE clients about restock approval and updated inventory
        try:
            notify_clients({
                'type': 'restock_update',
                'request_id': request_id,
                'status': 'approved',
                'medicine_id': request_record['medicine_id'],
                'medicine_name': request_record['medicine_name'],
                'added_quantity': request_record['requested_quantity'],
                'old_quantity': old_quantity,
                'new_quantity': new_quantity,
                'approved_by': actor_id
            })
        except Exception:
            pass
        return jsonify({
            'message': 'Restock request approved and inventory updated',
            'old_quantity': old_quantity,
            'new_quantity': new_quantity,
            'added_quantity': request_record['requested_quantity'],
            'medicine_name': request_record['medicine_name']
        }), 200
    except Exception as e:
        print(f"Error approving restock request: {e}")
        return jsonify({'message': str(e)}), 500


@app.route('/api/admin/restock-request/<int:request_id>/reject', methods=['PUT'])
def api_reject_restock_request(request_id):
    """Admin rejects restock request"""
    try:
        data = request.json or {}
        actor_id = data.get('actor_id')
        role = _get_user_role(actor_id) if actor_id else None
        if role != 'admin':
            return jsonify({'message': 'Only admin can reject requests'}), 403

        rejection_reason = data.get('rejection_reason', 'Request rejected').strip()

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database error'}), 500
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE restock_requests 
            SET status = 'rejected', approved_by = %s, approved_at = NOW(), admin_notes = %s
            WHERE id = %s
        ''', (actor_id, rejection_reason, request_id))

        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"OK - Restock request {request_id} rejected by admin {actor_id}: {rejection_reason}")
        # Notify clients that request was rejected
        try:
            notify_clients({
                'type': 'restock_update',
                'request_id': request_id,
                'status': 'rejected',
                'reason': rejection_reason,
                'rejected_by': actor_id
            })
        except Exception:
            pass
        return jsonify({'message': 'Restock request rejected', 'reason': rejection_reason}), 200
    except Exception as e:
        print(f"Error rejecting restock request: {e}")
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("Hospital and community Pharmacy management - Server Starting")
    print("=" * 70)
    print("\nServer is starting...\n")
    print("Access the system at:")
    print("   http://localhost:5000/")
    print("   http://localhost:5000/hospital_landing.html")
    print("   http://localhost:5000/login.html")
    print("   http://localhost:5000/signup.html")
    print("   http://localhost:5000/pharmacist_portal.html")
    print("   http://localhost:5000/admin_portal.html")
    print("\nAPI Endpoints:")
    print("   POST /login")
    print("   POST /signup")
    print("   GET  /health")
    print("\n" + "=" * 70)
    print("Server running on http://0.0.0.0:5000/")
    print("Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    # Ensure tables exist before starting (creates if missing)
    try:
        ensure_medicines_table_exists()
        ensure_restock_table_exists()
        ensure_notifications_table_exists()
    except Exception as e:
        print(f"Warning: could not ensure tables: {e}")

    app.run(debug=False, host='0.0.0.0', port=5000)
