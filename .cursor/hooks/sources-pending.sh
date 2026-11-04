#!/usr/bin/env bash
# Cursor sessionStart hook: tell the agent when Zotero items are waiting for ingest.
# Prints {"additional_context": "..."} when something is waiting, otherwise {} (no credentials, Zotero
# unreachable, nothing waiting, or any error), and always exits 0.
timeout 2 cat >/dev/null 2>&1
cd "$(dirname "$0")/../.." || {
  echo '{}'
  exit 0
}
out=""
if command -v uv >/dev/null 2>&1 && [[ -x .venv/bin/python ]]; then
  # --no-sync: a stale .venv must not start a dependency sync, which outlasts the timeout.
  out=$(timeout 15 uv run --no-sync python -m lib.sources.cli pending --hook </dev/null 2>/dev/null)
fi
if [[ $out == \{* ]]; then
  printf '%s\n' "$out"
else
  echo '{}'
fi
exit 0
