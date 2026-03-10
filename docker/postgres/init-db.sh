#!/bin/bash
set -e

# This script runs when the postgres container is first initialized
# It creates the database and user if they don't exist

echo "Initializing database: ${POSTGRES_DB}"
echo "Initializing user: ${POSTGRES_USER}"

# Create user if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    SELECT 'CREATE USER ${POSTGRES_USER}'
    WHERE NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '${POSTGRES_USER}')\gexec

    ALTER USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';
    ALTER USER ${POSTGRES_USER} WITH SUPERUSER;
EOSQL

# Create database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    SELECT 'CREATE DATABASE ${POSTGRES_DB}'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${POSTGRES_DB}')\gexec

    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
EOSQL

echo "Database initialization complete"
