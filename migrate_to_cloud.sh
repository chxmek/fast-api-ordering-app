#!/bin/bash

# Cloud Database Migration Script
# Usage: ./migrate_to_cloud.sh <CLOUD_DATABASE_URL>

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Cloud database URL required"
    echo "Usage: ./migrate_to_cloud.sh 'postgresql://user:pass@host:port/db'"
    exit 1
fi

CLOUD_DB_URL="$1"
BACKUP_FILE="backups/pre_cloud_migration_$(date +%Y%m%d_%H%M%S).sql"

echo "🔄 Starting cloud migration..."
echo ""

# Step 1: Backup local database
echo "📦 Step 1/4: Creating local backup..."
mkdir -p backups
pg_dump -U mek -d ordering_db -f "$BACKUP_FILE"
echo "✅ Backup created: $BACKUP_FILE"
echo ""

# Step 2: Test cloud connection
echo "🔌 Step 2/4: Testing cloud connection..."
if psql "$CLOUD_DB_URL" -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ Cloud connection successful"
else
    echo "❌ Cannot connect to cloud database"
    echo "Please check your connection string"
    exit 1
fi
echo ""

# Step 3: Migrate schema and data
echo "📤 Step 3/4: Migrating data to cloud..."
psql "$CLOUD_DB_URL" < "$BACKUP_FILE"
echo "✅ Data migration complete"
echo ""

# Step 4: Verify migration
echo "🔍 Step 4/4: Verifying migration..."
TABLE_COUNT=$(psql "$CLOUD_DB_URL" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
echo "✅ Found $TABLE_COUNT tables in cloud database"

USER_COUNT=$(psql "$CLOUD_DB_URL" -t -c "SELECT count(*) FROM users;" 2>/dev/null || echo "0")
echo "✅ Migrated $USER_COUNT users"

echo ""
echo "🎉 Migration completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env file with new DATABASE_URL"
echo "2. Test application: uvicorn main:app --reload"
echo "3. Keep local backup: $BACKUP_FILE"
