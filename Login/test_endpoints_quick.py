#!/usr/bin/env python3
"""
Quick endpoint verification script
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Read server_patient_doctor.py and check for endpoints
try:
    with open('server_patient_doctor.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for new endpoints
    endpoints = [
        '/api/medicines',
        '/api/admin/users',
        '/api/admin/user/<int:user_id>/role',
        '/api/admin/settings'
    ]
    
    print("ENDPOINT VERIFICATION")
    print("=" * 60)
    
    for endpoint in endpoints:
        if endpoint in content:
            print(f"✓ {endpoint} - Found")
        else:
            print(f"✗ {endpoint} - NOT FOUND")
    
    # Check for key functions
    functions = [
        'ensure_medicines_table_exists',
        '_get_user_role',
        'def get_db_connection'
    ]
    
    print("\nFUNCTION VERIFICATION")
    print("=" * 60)
    
    for func in functions:
        if func in content:
            print(f"✓ {func} - Found")
        else:
            print(f"✗ {func} - NOT FOUND")
    
    # Check for dashboard files
    dashboards = [
        'pharmacist_dashboard.html',
        'admin_dashboard.html'
    ]
    
    print("\nDASHBOARD FILES")
    print("=" * 60)
    
    for dashboard in dashboards:
        if os.path.exists(dashboard):
            with open(dashboard, 'r', encoding='utf-8') as f:
                dashboard_content = f.read()
            
            # Check for API calls
            if '/api/' in dashboard_content:
                print(f"✓ {dashboard} - Contains API calls")
            else:
                print(f"✗ {dashboard} - No API calls found")
        else:
            print(f"✗ {dashboard} - FILE NOT FOUND")
    
    print("\n" + "=" * 60)
    print("Verification complete!")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
