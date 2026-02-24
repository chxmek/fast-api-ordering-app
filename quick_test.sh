#!/usr/bin/env python3
"""Quick API endpoint test"""
import subprocess
import json

endpoints = [
    ("GET", "/health", None),
    ("POST", "/auth/login", '{"email":"mek@email.com","password":"password123"}'),
    ("GET", "/menu/items", None),
    ("GET", "/orders", None),
]

base_url = "http://127.0.0.1:8001"

print("\n📡 Testing API Endpoints\n")

for method, path, data in endpoints:
    if method == "GET":
        cmd = f'curl -s -o /dev/null -w "%{{http_code}}" {base_url}{path}'
    else:
        cmd = f'curl -s -o /dev/null -w "%{{http_code}}" -X {method} -H "Content-Type: application/json" -d \'{data}\' {base_url}{path}'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    status = result.stdout.strip()
    
    symbol = "✓" if status.startswith("2") else "✗"
    print(f"{symbol} {method:4} {path:30} - Status: {status}")

print("\n✓ API endpoint test complete\n")
