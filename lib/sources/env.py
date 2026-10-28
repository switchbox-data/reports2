"""Environment and local cache locations shared by the source-ingest modules.

Credentials come from the repo's ``.env`` (gitignored) or the process environment; none is ever printed.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "context" / "sources"
REPORTS_DIR = REPO_ROOT / "reports"
REFERENCES_YAML = REPORTS_DIR / "references.yaml"

# Variables the pipeline reads, by service. ``doctor`` checks each one.
VARIABLES: dict[str, tuple[str, ...]] = {
    "zotero": ("ZOTERO_API_KEY", "ZOTERO_GROUP_ID"),
    "documentcloud": ("DOCUMENTCLOUD_USERNAME", "DOCUMENTCLOUD_PASSWORD"),
    "gdrive": ("GDRIVE_SERVICE_ACCOUNT_JSON", "GDRIVE_PUBLIC_FOLDER_ID"),
    "wayback": ("IA_ACCESS_KEY", "IA_SECRET_KEY"),
    "contact": ("SOURCES_CONTACT_EMAIL",),
}


def cache_dir() -> Path:
    """Scratch space for inbox downloads, fetched PDFs, ingest cards, write logs and the ``pub`` clone."""
    return Path(os.environ.get("SOURCES_CACHE_DIR", "~/.cache/switchbox_sources")).expanduser()


def load_env() -> None:
    """Load ``.env`` from the repo root (does not override variables already set)."""
    load_dotenv(REPO_ROOT / ".env")


def get(name: str) -> str | None:
    """A variable's value after loading ``.env``; ``None`` when unset or empty."""
    load_env()
    return os.environ.get(name) or None


def missing(names: tuple[str, ...]) -> list[str]:
    """The names among ``names`` that are unset or empty."""
    load_env()
    return [n for n in names if not os.environ.get(n)]


def require(*names: str) -> None:
    """Raise a clear error naming every variable in ``names`` that is unset."""
    if gone := missing(names):
        raise RuntimeError(f"Set {' and '.join(gone)} in {REPO_ROOT / '.env'}")
