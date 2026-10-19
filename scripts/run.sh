#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt
(cd frontend && npm ci && npm run build)
if [ "${ALLOW_LIVE_MODEL:-0}" = "1" ]; then
  .venv/bin/python -m backend.warm_model
fi
exec .venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
