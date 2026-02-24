#!/usr/bin/env python3
"""Comprehensive API Endpoint Validator"""
import subprocess
import json

endpoints = [
    # Health
    ("GET", "/health", None, 200),
    # Auth
    ("POST", "/api/v1/auth/login", '{"email":"mek@email.com","password":"password123"}', 200),
    # Menu
    ("GET", "/api/v1/menu/items", None, 200),
    ("GET", "/api/v1/menu/categories", None, 200),
    ("GET", "/api/v1/menu/options", None, 200),
    # Orders
    ("GET", "/api/v1/orders", None, 200),
    # Users
    ("GET", "/api/v1/users/", None, [200, 403]),
    # Admin
    ("GET", "/api/v1/admin/dashboard/stats", None, [200, 403]),
    # SuperAdmin
    ("GET", "/api/v1/superadmin/roles/summary", None, [200, 403]),
]

base_url = "http://127.0.0.1:8001"

print("\n" + "="*70)
print("  🚀 FastAPI Ordering System - API Endpoint Validator")
print("="*70 + "\n")

passed = 0
failed = 0

for method, path, data, expected in endpoints:
    if isinstance(expected, list):
        expected_codes = expected
    else:
        expected_codes = [expected]
    
    if method == "GET":
        cmd = f'curl -s -o /dev/null -w "%{{http_code}}" {base_url}{path}'
    else:
        if data:
            cmd = f'curl -s -o /dev/null -w "%{{http_code}}" -X {method} -H "Content-Type: application/json" -d \'{data}\' {base_url}{path}'
        else:
            cmd = f'curl -s -o /dev/null -w "%{{http_code}}" -X {method} {base_url}{path}'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    status = int(result.stdout.strip())
    
    is_success = status in expected_codes
    symbol = "✓" if is_success else "✗"
    
    if is_success:
        passed += 1
        status_text = f"✓ {status}"
    else:
        failed += 1
        status_text = f"✗ {status} (expected {expected_codes})"
    
    print(f"{symbol} {method:6} {path:40} → {status_text}")

print("\n" + "="*70)
print(f"  Results: {passed} passed ✓ | {failed} failed ✗")
print("="*70 + "\n")

if failed == 0:
    print("✓ All critical endpoints are working!\n")
else:
    print(f"⚠ {failed} endpoints need attention\n")
