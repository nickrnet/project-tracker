#!/usr/bin/env bash
set -euo pipefail

# dev_psql.sh - helper to open a psql shell against the project's Postgres
# service (running via docker-compose) or to run a one-off SQL command.
#
# Usage:
#   ./dev_psql.sh                # interactive psql against the app DB
#   ./dev_psql.sh -c "SELECT 1;"  # run a command and exit

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$ROOT_DIR"

# Load simple KEY=VALUE pairs from .env
if [ -f .env ]; then
  # shellcheck disable=SC2046
  eval $(grep -v '^\s*#' .env | sed -E 's/"/\\"/g' | xargs -I{} echo export {} ) || true
fi

echo "Connecting to project Postgres..."

# If DATABASE_URL explicitly points to postgres, use the app container to run psql
if [ -n "${DATABASE_URL:-}" ] && [[ "${DATABASE_URL}" == postgres:* ]]; then
  echo "Using DATABASE_URL from .env"
  docker-compose exec django psql "${DATABASE_URL}" ${@+"$@"}
  exit $?
fi

# Otherwise try to connect to the postgres service directly
PG_USER="${POSTGRES_USER:-tracker}"
PG_DB="${POSTGRES_DB:-tracker}"

if docker-compose ps | grep -q "postgres"; then
  docker-compose exec postgres psql -U "$PG_USER" -d "$PG_DB" ${@+"$@"}
  exit $?
else
  echo "Postgres service not running. Start it with: docker-compose up -d postgres" >&2
  exit 2
fi
