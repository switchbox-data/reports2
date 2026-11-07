"""Check that every GitHub permalink in a provenance document resolves (opt-in: ``--check-links``).

A link 404s when its tag hasn't been pushed, or when a path doesn't exist at the tag. Each
``github.com/<org>/<repo>/(blob|tree)/<ref>/<path>`` URL is checked with
``gh api repos/<org>/<repo>/contents/<path>?ref=<ref>``, which answers for files and folders alike.
A ref may contain slashes (tags like ``mc/1b1b329be68f``), so the URL can't say where it ends; the
first one to three segments are tried as the ref, and the link resolves if any split does.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable

from lib.provenance.review import Review, flag

GITHUB_URL_RE = re.compile(r"https://github\.com/([^/\s]+)/([^/\s]+)/(?:blob|tree)/([^#?)\s\]]+)")
MAX_REF_SEGMENTS = 3


def parse_github_url(url: str) -> tuple[str, str, str] | None:
    """``(org, repo, "<ref>/<path>")`` of a GitHub blob/tree URL, without any ``#L..`` fragment."""
    m = GITHUB_URL_RE.match(url)
    return None if m is None else (m.group(1), m.group(2), m.group(3).rstrip("/"))


def find_urls(text: str) -> list[str]:
    return [m.group(0) for m in GITHUB_URL_RE.finditer(text)]


def _exists(org: str, repo: str, ref: str, path: str) -> bool:
    api = f"repos/{org}/{repo}/contents/{path}?ref={ref}"
    return subprocess.run(["gh", "api", api, "--silent"], capture_output=True, text=True).returncode == 0


def _resolves(org: str, repo: str, ref_and_path: str) -> bool:
    parts = ref_and_path.split("/")
    return any(
        _exists(org, repo, "/".join(parts[:k]), "/".join(parts[k:]))
        for k in range(1, min(MAX_REF_SEGMENTS, len(parts)) + 1)
    )


def check_links(urls: Iterable[str], review: Review) -> None:
    targets = sorted({t for u in urls if (t := parse_github_url(u)) is not None})
    missing = 0
    for org, repo, ref_and_path in targets:
        if not _resolves(org, repo, ref_and_path):
            missing += 1
            flag(review, "link_missing", f"{org}/{repo}", f"{ref_and_path} not found on GitHub")
    flag(review, "links_checked", str(len(targets)), f"files and folders linked; {missing} not found")
