"""Fetch files from the rate-design-platform GitHub repo and parse URDB tariff JSON."""

from __future__ import annotations

import base64
import json
import os
import urllib.request


def fetch_rdp_file(path: str, ref: str) -> str:
    """Fetch a file from rate-design-platform on GitHub; return contents as string.

    Uses the GitHub API with ``GITHUB_TOKEN`` when available (required for
    private repos), otherwise falls back to the public raw URL.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        url = f"https://api.github.com/repos/switchbox-data/rate-design-platform/contents/{path}?ref={ref}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        return base64.b64decode(data["content"]).decode()
    url = f"https://raw.githubusercontent.com/switchbox-data/rate-design-platform/{ref}/{path}"
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode()


def parse_urdb_json(content: str | bytes) -> dict:
    """Parse URDB tariff JSON (string or bytes) into a dict."""
    if isinstance(content, bytes):
        content = content.decode()
    return json.loads(content)
