#!/usr/bin/env python3
"""Test JavaScript date comparison logic for expiring medicines"""

from datetime import datetime, timedelta

def test_date_logic():
    """Test the date logic that will be used in JavaScript"""
    today = datetime.now().date()
    
    # JavaScript logic: new Date(today.getFullYear(), today.getMonth() + 1, 0)
    # This creates a date with year=today.year, month=today.month+1, day=0
    # day=0 means last day of the previous month
    # So this gives us the last day of the current month
    
    # Python equivalent: create last day of this month
    if today.month == 12:
        this_month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
    else:
        this_month_end = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
    
    three_months_later = today + timedelta(days=90)
    
    print("Date Logic Testing:")
    print(f"Today: {today}")
    print(f"This Month End: {this_month_end}")
    print(f"Three Months Later: {three_months_later}")
    print()
    
    # Test cases
    test_dates = [
        ("2025-12-31", "expired"),      # Old date
        ("2026-01-15", "expired"),      # Past date
        ("2026-02-28", "critical"),     # End of this month
        ("2026-03-15", "upcoming"),     # Within 3 months
        ("2026-05-19", "upcoming"),     # Around 3 months
        ("2026-05-20", "safe"),         # Beyond 3 months
        ("2027-06-30", "safe"),         # Far future
    ]
    
    print("Test Cases:")
    for date_str, expected in test_dates:
        exp_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        if exp_date < today:
            actual = "expired"
        elif exp_date <= this_month_end:
            actual = "critical"
        elif exp_date <= three_months_later:
            actual = "upcoming"
        else:
            actual = "safe"
        
        status = "✓" if actual == expected else "✗"
        print(f"  {status} {date_str}: {actual} (expected: {expected})")

if __name__ == "__main__":
    test_date_logic()
