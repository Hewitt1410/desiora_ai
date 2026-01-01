#!/bin/bash

# Backup script for database and volumes
# Usage: ./scripts/backup.sh

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"

mkdir -p "$BACKUP_PATH"

echo "Starting backup..."

# Backup PostgreSQL database
echo "Backing up PostgreSQL database..."
docker-compose exec -T postgres pg_dump -U desiora desiora > "$BACKUP_PATH/database.sql"

# Backup volumes
echo "Backing up volumes..."
docker run --rm \
    -v desiora_ai_postgres_data:/data \
    -v "$(pwd)/$BACKUP_PATH":/backup \
    alpine tar czf /backup/postgres_data.tar.gz -C /data .

docker run --rm \
    -v desiora_ai_redis_data:/data \
    -v "$(pwd)/$BACKUP_PATH":/backup \
    alpine tar czf /backup/redis_data.tar.gz -C /data .

# Create archive
echo "Creating backup archive..."
tar czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" -C "$BACKUP_PATH" .

# Remove temporary files
rm -rf "$BACKUP_PATH"

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Keep only last 7 backups
echo "Cleaning old backups..."
ls -t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup cleanup completed!"


