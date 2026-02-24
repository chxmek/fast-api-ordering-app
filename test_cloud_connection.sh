#!/bin/bash

# Quick Cloud Setup Test Script
# Tests connection to cloud database

set -e

echo "🔍 Cloud Database Connection Test"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    echo "Please create .env from .env.example"
    exit 1
fi

# Load environment variables
source .env 2>/dev/null || true

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set in .env"
    exit 1
fi

echo "📡 Testing connection to:"
echo "  $(echo $DATABASE_URL | sed 's/:\/\/.*@/:\/\/***:***@/')"
echo ""

# Test with Python
cd /Users/mekchawanwit/Desktop/Dev/ordering_fls_app/back-end/fastapi-ordering

source venv/bin/activate

python3 << 'EOF'
import os
from sqlalchemy import create_engine, text

try:
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ Connection successful!")
        print(f"📊 PostgreSQL version: {version.split(',')[0]}")
        
        # Count tables
        result = conn.execute(text("""
            SELECT count(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """))
        table_count = result.fetchone()[0]
        print(f"📋 Tables found: {table_count}")
        
        # Check users table
        try:
            result = conn.execute(text("SELECT count(*) FROM users;"))
            user_count = result.fetchone()[0]
            print(f"👥 Users in database: {user_count}")
        except:
            print("⚠️  Users table not found (might need migration)")
            
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    exit(1)
EOF

echo ""
echo "🎉 Cloud database is ready!"
