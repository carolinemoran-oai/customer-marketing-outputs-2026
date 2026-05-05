#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=8501}"
: "${SERVER_NAME:=localhost}"

if [ -x ".venv/bin/streamlit" ]; then
  STREAMLIT=".venv/bin/streamlit"
else
  STREAMLIT="streamlit"
fi

exec "$STREAMLIT" run app.py \
  --server.headless true \
  --server.address 0.0.0.0 \
  --server.port "$PORT" \
  --browser.serverAddress "$SERVER_NAME"
