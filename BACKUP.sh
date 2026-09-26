#!/usr/bin/env bash
set -e

cd /home/ubuntu/Ardent

BACKUP_DIR="/home/ubuntu/Ardent/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

mkdir -p "$BACKUP_DIR"

sqlite3 storage/data/ardent.db \
  ".backup '$BACKUP_DIR/ardent-$TIMESTAMP.db'"

find "$BACKUP_DIR" -type f -name "ardent-*.db" -mtime +7 -delete

echo "Backup complete: $BACKUP_DIR/ardent-$TIMESTAMP.db"