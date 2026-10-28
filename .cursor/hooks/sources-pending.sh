#!/usr/bin/env bash
# Session start: tell the agent when Zotero items are waiting for ingest.
# Prints nothing (and exits 0) when nothing is waiting, credentials are missing, or Zotero is unreachable.
cd "$(dirname "$0")/../.." || exit 0
command -v uv >/dev/null 2>&1 || exit 0
timeout 15 uv run python -m lib.sources.cli pending --hook 2>/dev/null || true
exit 0
