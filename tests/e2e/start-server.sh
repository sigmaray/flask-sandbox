#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

set -a
# shellcheck source=/dev/null
source "$ROOT/.env.e2e"
set +a

source venv/bin/activate
export FLASK_APP=app.py
export PYTHONPATH="$ROOT"

if command -v psql >/dev/null 2>&1; then
  DB_NAME="${DATABASE_URL##*/}"
  ADMIN_URL="${DATABASE_URL%/*}/postgres"
  if ! psql "$ADMIN_URL" -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1; then
    psql "$ADMIN_URL" -c "CREATE DATABASE \"${DB_NAME}\""
  fi
fi

python scripts/e2e-setup.py
exec flask run --host 127.0.0.1 --port "${E2E_PORT}" --no-debugger --no-reload
