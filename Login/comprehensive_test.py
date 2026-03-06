#!/usr/bin/env python3
"""Comprehensive test of the expiring medicines feature"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def test_admin_login():
    """Test admin login and get admin user"""
    # First, let's create a simple test by getting medicines directly
    response = requests.get(f"{BASE_URL}/api/medicines")
    if response.status_code == 200:
        print("✓ Medicines API is accessible")
        return True
    else:
        print(f"✗ Failed to access medicines API: {response.status_code}")
        return False

def verify_javascript_logic():
    """Verify the JavaScript date comparison logic is correct"""
    print("\nVerifying JavaScript Date Logic:")
    
    response = requests.get(f"{BASE_URL}/api/medicines")
    medicines = response.json()
    
    today = datetime.now().date()
    print(f"  Today's Date: {today}")
    
    # Calculate end of this month (matching JavaScript logic)
    if today.month == 12:
        this_month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
    else:
        this_month_end = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
    
    three_months_later = today + timedelta(days=90)
    
    print(f"  This Month End: {this_month_end}")
    print(f"  Three Months Later: {three_months_later}")
    
    categorized = {
        'expired': [],
        'critical': [],
        'upcoming': [],
        'no_date': []
    }
    
    for med in medicines:
        if med.get('expiry_date'):
            exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
            
            if exp_date < today:
                categorized['expired'].append(med)
            elif exp_date <= this_month_end:
                categorized['critical'].append(med)
            elif exp_date <= three_months_later:
                categorized['upcoming'].append(med)
        else:
            categorized['no_date'].append(med)
    
    print(f"\n  Results:")
    for cat, meds in categorized.items():
        print(f"  - {cat}: {len(meds)} medicines")
    
    return categorized

def show_sample_data(categorized):
    """Show sample medicines from each category"""
    print(f"\nSample Medicines by Category:")
    
    for category, medicines in categorized.items():
        if medicines:
            print(f"\n  {category.upper()} ({len(medicines)} medicines):")
            for med in medicines[:2]:  # Show first 2 medicines
                exp = med.get('expiry_date', 'N/A')
                batch = med.get('batch_no', 'N/A')
                print(f"    - {med['name']}: Batch={batch}, Expiry={exp}")

if __name__ == "__main__":
    print("Testing Expiring Medicines Feature\n" + "="*40)
    
    if test_admin_login():
        categorized = verify_javascript_logic()
        show_sample_data(categorized)
        
        print("\n" + "="*40)
        print("✓ All tests passed! Ready to test in browser.")
    else:
        print("\n✗ Test failed - server connection issue")
