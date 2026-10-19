#!/bin/sh
set -e

# Schema must exist before the API takes traffic (service does not auto-create tables).
alembic upgrade head

# Allow PORT from the environment (common on PaaS); default matches Dockerfile/CMD.
if [ "$1" = "uvicorn" ] && [ -n "${PORT}" ]; then
  set -- uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
fi

exec "$@"
