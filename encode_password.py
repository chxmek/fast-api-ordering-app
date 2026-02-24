#!/usr/bin/env python3
"""
URL Encode Password Helper
Encodes special characters in password for PostgreSQL connection string
"""

import urllib.parse
import sys

def encode_password(password):
    """Encode password for use in PostgreSQL connection string."""
    return urllib.parse.quote(password, safe='')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encode_password.py 'your_password'")
        print("\nExample:")
        print("  python encode_password.py 'Mm6229744!@'")
        print("\nOutput will be URL-encoded password for connection string")
        sys.exit(1)
    
    password = sys.argv[1]
    encoded = encode_password(password)
    
    print(f"Original password: {password}")
    print(f"Encoded password:  {encoded}")
    print(f"\nUse in connection string:")
    print(f"postgresql://postgres:{encoded}@db.xxx.supabase.co:5432/postgres")
