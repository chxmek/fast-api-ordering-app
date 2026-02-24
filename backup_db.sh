#!/bin/bash

# PostgreSQL Database Backup Script
# Usage: ./backup_db.sh

set -e

# Configuration
DB_USER="mek"
DB_NAME="ordering_db"
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Backup filename
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"
COMPRESSED_FILE="$BACKUP_FILE.gz"

echo "🔄 Starting backup of $DB_NAME..."

# Create backup
pg_dump -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

echo "✅ Backup completed: $COMPRESSED_FILE"
echo "📦 Backup size: $(du -h "$COMPRESSED_FILE" | cut -f1)"

# Keep only last 7 backups (optional)
echo "🧹 Cleaning old backups (keeping last 7)..."
ls -t "$BACKUP_DIR"/*.sql.gz | tail -n +8 | xargs -r rm --

echo "✅ Backup process finished!"
echo "📁 Backup location: $COMPRESSED_FILE"
