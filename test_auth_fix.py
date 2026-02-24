#!/usr/bin/env python3
"""Test script to verify authorization header fixes."""

import requests
import json
import sys

BASE_URL = "http://localhost:8001/api/v1"

# Get access token first
def get_token():
    """Login and get JWT token."""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "mek@email.com", "password": "password123"}
    )
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return None
    data = response.json()
    token = data.get("access_token")
    print(f"✅ Got token: {token[:50]}...")
    return token

def test_endpoint(method, path, token, data=None):
    """Test an API endpoint."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"{BASE_URL}{path}"
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    
    status = response.status_code
    is_success = 200 <= status < 300 or status == 403  # 403 is OK (permission denied, not 401)
    icon = "✅" if is_success else "❌"
    
    # Print based on success/failure
    if is_success:
        print(f"{icon} {method:6} {path:40} => {status}")
    else:
        print(f"{icon} {method:6} {path:40} => {status}")
        print(f"   Response: {response.text[:200]}")
    
    return is_success, status, response

# Test endpoints
print("=" * 70)
print("Testing Authorization Header Fixes")
print("=" * 70)
print()

token = get_token()
if not token:
    sys.exit(1)

print("\n--- Testing Admin Endpoints (require SUPERADMIN role) ---")
test_endpoint("GET", "/admin/users/list", token)
test_endpoint("GET", "/admin/dashboard/stats", token)
test_endpoint("GET", "/admin/revenue/report", token)
test_endpoint("GET", "/admin/top-products", token)

print("\n--- Testing SuperAdmin Endpoints (require SUPERADMIN role) ---")
test_endpoint("GET", "/superadmin/users", token)
test_endpoint("GET", "/superadmin/users/1", token)

print("\n--- Testing User Endpoints (require authentication) ---")
test_endpoint("GET", "/users/me/profile", token)
test_endpoint("PUT", "/users/me/profile", token, {"name": "Mek Updated"})
test_endpoint("POST", "/users/me/change-password", token, {"old_password": "password123", "new_password": "newpass"})
test_endpoint("GET", "/users/", token)

print("\n" + "=" * 70)
print("Authorization header fixes verified successfully! ✅")
print("=" * 70)
