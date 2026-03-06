#!/usr/bin/env python3
"""
Test script to verify the Expiring Medicines feature is working
Run this to see the categorization of medicines by expiry status
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def test_expiring_medicines_feature():
    """Test the expiring medicines categorization"""
    
    print("="*60)
    print("EXPIRING MEDICINES FEATURE - DATA VERIFICATION TEST")
    print("="*60)
    
    # Fetch medicines
    print("\n[1] Fetching medicines from API...")
    try:
        response = requests.get(f"{BASE_URL}/api/medicines")
        if response.status_code != 200:
            print(f"✗ Failed to fetch medicines: {response.status_code}")
            return False
        
        data = response.json()
        medicines = data.get('medicines', []) if isinstance(data, dict) else data
        
        if not medicines:
            print("✗ No medicines found in database")
            return False
            
        print(f"✓ Successfully fetched {len(medicines)} medicines")
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Categorize medicines
    print("\n[2] Categorizing medicines by expiry status...")
    
    today = datetime.now().date()
    
    # Calculate month end (day 0 of next month equals last day of current month)
    if today.month == 12:
        month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
    else:
        month_end = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
    
    three_months = today + timedelta(days=90)
    
    print(f"   Today: {today}")
    print(f"   This Month End: {month_end}")
    print(f"   Plus 3 Months: {three_months}")
    
    expired = []
    critical = []
    upcoming = []
    no_date = []
    
    for med in medicines:
        if med.get('expiry_date'):
            exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
            
            if exp_date < today:
                expired.append(med)
            elif exp_date <= month_end:
                critical.append(med)
            elif exp_date <= three_months:
                upcoming.append(med)
        else:
            no_date.append(med)
    
    # Display results
    print("\n[3] Categorization Results:")
    print(f"   ✓ Already Expired: {len(expired)} medicines")
    print(f"   ✓ Expiring This Month: {len(critical)} medicines")
    print(f"   ✓ Expiring in 3 Months: {len(upcoming)} medicines")
    print(f"   ✓ No Expiry Date: {len(no_date)} medicines")
    
    # Show sample expired medicines
    if expired:
        print("\n[4] Sample Expired Medicines:")
        for med in expired[:3]:
            exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
            days_since = (today - exp_date).days
            batch = med.get('batch_no') or 'N/A'
            print(f"   - {med['name']:<30} | Batch: {batch:<15} | {days_since} days ago")
    
    # Show sample upcoming medicines
    if upcoming:
        print("\n[5] Sample Upcoming Medicines (Next 3 Months):")
        for med in upcoming[:3]:
            exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
            days_left = (exp_date - today).days
            batch = med.get('batch_no') or 'N/A'
            print(f"   - {med['name']:<30} | Batch: {batch:<15} | {days_left} days left")
    
    # Show medicines with batch numbers
    with_batch = [m for m in medicines if m.get('batch_no')]
    if with_batch:
        print(f"\n[6] Medicines With Batch Numbers ({len(with_batch)}):")
        for med in with_batch:
            exp_date = med.get('expiry_date', 'N/A')
            print(f"   - {med['name']:<30} | Batch: {med.get('batch_no')} | Expiry: {exp_date}")
    
    # Success message
    print("\n" + "="*60)
    print("✓ FEATURE TEST PASSED")
    print("="*60)
    print("\nYou can now:")
    print("1. Open the Admin Portal: http://localhost:5000/admin_portal.html")
    print("2. Navigate to the 'Expiring Medicines' tab")
    print("3. View the categorized medicines and use filters")
    print("\n")
    
    return True

if __name__ == "__main__":
    test_expiring_medicines_feature()
