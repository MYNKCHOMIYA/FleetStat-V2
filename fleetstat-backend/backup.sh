#!/bin/bash
# ============================================================
# FleetStat Database — Backup Script
# ============================================================
# Usage:
#   ./backup.sh              → Create a timestamped backup
#   ./backup.sh restore      → Restore the latest backup
#   ./backup.sh restore FILE → Restore a specific backup file
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BACKUP_DIR="$SCRIPT_DIR/backups"
mkdir -p "$BACKUP_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

case "${1:-backup}" in
  backup|"")
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/fleetstat_backup_${TIMESTAMP}.sql"
    
    echo -e "${YELLOW}Creating database backup...${NC}"
    PGPASSWORD=admin pg_dump \
      -h localhost -p 5433 \
      -U postgres -d fleetstat \
      --no-owner --no-acl \
      > "$BACKUP_FILE"
    
    # Remove restrict lines if present
    sed -i '/^\\restrict/d; /^\\unrestrict/d' "$BACKUP_FILE"
    
    SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✓ Backup created: $BACKUP_FILE ($SIZE)${NC}"
    
    # Keep only last 10 backups
    ls -t "$BACKUP_DIR"/fleetstat_backup_*.sql 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
    echo -e "${GREEN}✓ Backup rotation: keeping last 10 backups${NC}"
    ;;
    
  restore)
    if [ -n "$2" ]; then
      RESTORE_FILE="$2"
    else
      RESTORE_FILE=$(ls -t "$BACKUP_DIR"/fleetstat_backup_*.sql 2>/dev/null | head -1)
    fi
    
    if [ -z "$RESTORE_FILE" ] || [ ! -f "$RESTORE_FILE" ]; then
      echo -e "${RED}No backup file found to restore.${NC}"
      exit 1
    fi
    
    echo -e "${YELLOW}Restoring from: $RESTORE_FILE${NC}"
    echo -e "${RED}WARNING: This will overwrite the current database!${NC}"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      PGPASSWORD=admin psql \
        -h localhost -p 5433 \
        -U postgres -d fleetstat \
        < "$RESTORE_FILE"
      echo -e "${GREEN}✓ Database restored successfully!${NC}"
    else
      echo "Cancelled."
    fi
    ;;
    
  *)
    echo "Usage: ./backup.sh [backup|restore [FILE]]"
    exit 1
    ;;
esac
