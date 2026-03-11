#!/bin/bash
# This script ensures the database exists before running migrations
# It runs on every container startup, not just first initialization

set -e

DB_NAME="${POSTGRES_DB:-tracker}"
DB_USER="${POSTGRES_USER:-tracker}"
DB_PASS="${POSTGRES_PASSWORD:-tracker}"

echo "Checking if database '$DB_NAME' exists..."

# Wait for PostgreSQL to be ready
until PGPASSWORD="$DB_PASS" psql -h postgres -U "$DB_USER" -d postgres -c '\q' 2>/dev/null; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "PostgreSQL is ready!"

# Check if database exists
DB_EXISTS=$(PGPASSWORD="$DB_PASS" psql -h postgres -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ "$DB_EXISTS" = "1" ]; then
  echo "Database '$DB_NAME' already exists."
else
  echo "Creating database '$DB_NAME'..."
  # Create the database - use CREATE DATABASE directly
  if PGPASSWORD="$DB_PASS" psql -h postgres -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\";" 2>&1 | grep -q "already exists"; then
    echo "Database '$DB_NAME' already exists (created by another service)."
  else
    echo "Database '$DB_NAME' created successfully!"
  fi
fi

echo "Database check complete. Ready to proceed..."
