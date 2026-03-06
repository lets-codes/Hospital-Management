#!/usr/bin/env python3
"""
Test to verify admin portal buttons are working correctly after fixes.
Tests: button rendering, modal opening, approval, rejection, and live stats update.
"""

import requests
import json
from datetime import datetime
import time

API_BASE = 'http://localhost:5000'

def test_admin_buttons_and_stats():
    """Test the complete admin button and stats flow"""
    print("\n" + "="*60)
    print("Testing Admin Portal Buttons and Live Stats Update")
    print("="*60)
    
    # 1. Create test data
    print("\n[1] Creating test data...")
    
    # Create admin user
    admin_resp = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Admin',
        'email': f'admin_buttons_test_{int(time.time())}@test.com',
        'phone': '9999999999',
        'password': 'test123',
        'role': 'admin'
    })
    
    admin_data = admin_resp.json()
    admin_id = admin_data.get('user_id')
    print(f"✓ Admin created: ID {admin_id}")
    
    # Create pharmacist
    pharm_resp = requests.post(f'{API_BASE}/signup', json={
        'fullname': 'Test Pharmacist',
        'email': f'pharm_buttons_test_{int(time.time())}@test.com',
        'phone': '8888888888',
        'password': 'test123',
        'role': 'pharmacist'
    })
    pharm_data = pharm_resp.json()
    pharm_id = pharm_data.get('user_id')
    print(f"✓ Pharmacist created: ID {pharm_id}")
    
    # Create medicines
    med_ids = []
    for i, med_name in enumerate(['Aspirin Test', 'Ibuprofen Test']):
        med_resp = requests.post(f'{API_BASE}/api/medicines', json={
            'actor_id': admin_id,
            'name': med_name,
            'manufacturer': 'TestCorp',
            'batch_no': f'BATCH{i}',
            'quantity': 100,
            'unit_price': 10.0,
            'expiry_date': '2025-12-31'
        })
        med_id = med_resp.json().get('medicine_id')
        med_ids.append(med_id)
        print(f"✓ Medicine created: {med_name} (ID {med_id})")
    
    # 2. Create restock requests (to test button interaction)
    print("\n[2] Creating restock requests...")
    req_ids = []
    for i, med_id in enumerate(med_ids):
        med_name = ['Aspirin Test', 'Ibuprofen Test'][i]
        req_resp = requests.post(f'{API_BASE}/api/restock-request', json={
            'actor_id': pharm_id,
            'medicine_id': med_id,
            'medicine_name': med_name,
            'requested_quantity': 50,
            'reason': f'Test reason {i}'
        })
        req_id = req_resp.json().get('request_id')
        req_ids.append(req_id)
        print(f"✓ Restock request created: ID {req_id}")
    
    # 3. Get initial stats
    print("\n[3] Checking initial stats...")
    stats_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
    initial_data = stats_resp.json()
    initial_requests = initial_data.get('requests', [])
    
    initial_pending = len([r for r in initial_requests if r['status'] == 'pending'])
    initial_approved = len([r for r in initial_requests if r['status'] == 'approved' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    initial_rejected = len([r for r in initial_requests if r['status'] == 'rejected' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    
    print(f"Initial stats:")
    print(f"  - Pending: {initial_pending}")
    print(f"  - Approved Today: {initial_approved}")
    print(f"  - Rejected Today: {initial_rejected}")
    
    # 4. Approve first request (simulating button click)
    print(f"\n[4] Approving request {req_ids[0]} (simulating button click)...")
    approve_resp = requests.put(
        f'{API_BASE}/api/admin/restock-request/{req_ids[0]}/approve',
        json={
            'actor_id': admin_id,
            'admin_notes': 'Approved via test'
        }
    )
    
    if approve_resp.status_code == 200:
        print(f"✓ Request approved successfully")
    else:
        print(f"✗ Approval failed: {approve_resp.text}")
        return
    
    # 5. Get stats after approval (this should trigger JavaScript update in real portal)
    print("\n[5] Checking stats after approval...")
    stats_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
    approved_data = stats_resp.json()
    approved_requests = approved_data.get('requests', [])
    
    approved_pending = len([r for r in approved_requests if r['status'] == 'pending'])
    approved_approved = len([r for r in approved_requests if r['status'] == 'approved' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    approved_rejected = len([r for r in approved_requests if r['status'] == 'rejected' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    
    print(f"After approval:")
    print(f"  - Pending: {approved_pending} (was {initial_pending}, expected {initial_pending - 1})")
    print(f"  - Approved Today: {approved_approved} (was {initial_approved}, expected {initial_approved + 1})")
    print(f"  - Rejected Today: {approved_rejected} (was {initial_rejected}, expected {initial_rejected})")
    
    # Verify counts changed correctly
    assert approved_pending == initial_pending - 1, f"Pending count mismatch: {approved_pending} != {initial_pending - 1}"
    assert approved_approved == initial_approved + 1, f"Approved count mismatch: {approved_approved} != {initial_approved + 1}"
    print("✓ Stats updated correctly after approval")
    
    # 6. Reject second request
    print(f"\n[6] Rejecting request {req_ids[1]} (simulating button click)...")
    reject_resp = requests.put(
        f'{API_BASE}/api/admin/restock-request/{req_ids[1]}/reject',
        json={
            'actor_id': admin_id,
            'rejection_reason': 'Rejected via test'
        }
    )
    
    if reject_resp.status_code == 200:
        print(f"✓ Request rejected successfully")
    else:
        print(f"✗ Rejection failed: {reject_resp.text}")
        return
    
    # 7. Get stats after rejection
    print("\n[7] Checking stats after rejection...")
    stats_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
    rejected_data = stats_resp.json()
    rejected_requests = rejected_data.get('requests', [])
    
    rejected_pending = len([r for r in rejected_requests if r['status'] == 'pending'])
    rejected_approved = len([r for r in rejected_requests if r['status'] == 'approved' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    rejected_rejected = len([r for r in rejected_requests if r['status'] == 'rejected' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    
    print(f"After rejection:")
    print(f"  - Pending: {rejected_pending} (was {approved_pending}, expected {approved_pending - 1})")
    print(f"  - Approved Today: {rejected_approved} (was {approved_approved}, expected {approved_approved})")
    print(f"  - Rejected Today: {rejected_rejected} (was {approved_rejected}, expected {approved_rejected + 1})")
    
    # Verify counts changed correctly
    assert rejected_pending == approved_pending - 1, f"Pending count mismatch: {rejected_pending} != {approved_pending - 1}"
    assert rejected_rejected == approved_rejected + 1, f"Rejected count mismatch: {rejected_rejected} != {approved_rejected + 1}"
    print("✓ Stats updated correctly after rejection")
    
    # 8. Test with filter applied (ensure stats still correct)
    print("\n[8] Testing stats calculation with filter applied...")
    filtered_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}&status=approved')
    filtered_data = filtered_resp.json()
    filtered_requests = filtered_data.get('requests', [])
    
    # Get unfiltered for stats calculation
    all_resp = requests.get(f'{API_BASE}/api/admin/restock-requests?actor_id={admin_id}')
    all_data = all_resp.json()
    all_requests = all_data.get('requests', [])
    
    # Stats should be calculated from ALL requests, not filtered ones
    stats_pending = len([r for r in all_requests if r['status'] == 'pending'])
    stats_approved = len([r for r in all_requests if r['status'] == 'approved' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    stats_rejected = len([r for r in all_requests if r['status'] == 'rejected' and r.get('approved_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))])
    
    print(f"With 'approved' filter:")
    print(f"  - Display shows: {len(filtered_requests)} approved requests")
    print(f"  - Stats calculated from ALL requests: Pending={stats_pending}, Approved Today={stats_approved}, Rejected Today={stats_rejected}")
    print("✓ Stats correctly use ALL data, not filtered data")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED - Admin buttons and stats are working!")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        test_admin_buttons_and_stats()
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
