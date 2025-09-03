#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-4321}
ROOT_DIR=$(pwd)
SITE_DIR="./seo-portfolio"
REPORT="$ROOT_DIR/lighthouse-report.json"

echo "Building site..."
( cd "$SITE_DIR" && npm ci && npm run build )

echo "Starting preview server on port $PORT..."
( cd "$SITE_DIR" && npm run preview -- --port "$PORT" ) &
PREVIEW_PID=$!

echo "Waiting for preview to start..."
sleep 4

echo "Running Lighthouse (headless)..."
# Use npx lighthouse for portability. Requires Chrome in runner.
npx lighthouse "http://localhost:${PORT}" --quiet --chrome-flags="--headless" --output=json --output-path="$REPORT" || true

echo "Killing preview server (PID $PREVIEW_PID)..."
kill "$PREVIEW_PID" || true

echo "Saved Lighthouse JSON to $REPORT"
