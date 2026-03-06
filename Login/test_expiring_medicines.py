#!/usr/bin/env python3
"""Test the expiring medicines feature in admin portal"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

# Test data
def test_expiring_medicines():
    print("Testing Expiring Medicines Dashboard...")
    
    # Get all medicines to see current inventory
    print("\n1. Fetching all medicines...")
    response = requests.get(f"{BASE_URL}/api/medicines")
    if response.status_code == 200:
        result = response.json()
        
        # Handle both list and dict responses
        if isinstance(result, dict):
            medicines = result.get('medicines', result)
        elif isinstance(result, list):
            medicines = result
        else:
            print(f"Unexpected response format: {type(result)}")
            return False
        
        print(f"✓ Found {len(medicines)} medicines in inventory")
        
        # Categorize by expiry status
        today = datetime.now().date()
        # Calculate end of this month
        if today.month == 12:
            this_month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
        else:
            this_month_end = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
        
        three_months_later = today + timedelta(days=90)
        
        expired = []
        critical = []  # Expiring this month
        upcoming = []  # Expiring in 3 months
        
        for med in medicines:
            if med.get('expiry_date'):
                exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
                
                if exp_date < today:
                    expired.append(med)
                elif exp_date <= this_month_end:
                    critical.append(med)
                elif exp_date <= three_months_later:
                    upcoming.append(med)
        
        print(f"\n   Category Breakdown:")
        print(f"   - Already Expired: {len(expired)}")
        print(f"   - Expiring This Month: {len(critical)}")
        print(f"   - Expiring in 3 Months: {len(upcoming)}")
        
        # Show details of some expiring medicines
        if expired:
            print(f"\n   Expired Medicines:")
            for med in expired[:3]:
                exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
                days_ago = (today - exp_date).days
                print(f"   - {med['name']} (Batch: {med.get('batch_no', 'N/A')}) - Expired {days_ago} days ago")
        
        if critical:
            print(f"\n   Expiring This Month:")
            for med in critical[:3]:
                exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
                days_left = (exp_date - today).days
                print(f"   - {med['name']} (Batch: {med.get('batch_no', 'N/A')}) - {days_left} days left")
        
        if upcoming:
            print(f"\n   Expiring in 3 Months:")
            for med in upcoming[:3]:
                exp_date = datetime.strptime(med['expiry_date'], '%Y-%m-%d').date()
                days_left = (exp_date - today).days
                print(f"   - {med['name']} (Batch: {med.get('batch_no', 'N/A')}) - {days_left} days left")
        
        # Show all medicines for debugging
        print(f"\n   All Medicines in Database:")
        for med in medicines:
            print(f"   - {med.get('name')} | Batch: {med.get('batch_no', 'N/A')} | Expiry: {med.get('expiry_date', 'N/A')}")
        
        return True
    else:
        print(f"✗ Failed to fetch medicines: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    test_expiring_medicines()

