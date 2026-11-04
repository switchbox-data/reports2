"""Public copies of PDFs on DocumentCloud (a thin wrapper over ``python-documentcloud``).

Uploads are tagged with the citation key in DocumentCloud's key-value data (``data_citekey``), so a rerun can
find a document whose ID was never recorded on the Zotero item. Only verified organizations can publish
publicly; ``just sources-doctor`` shows the account's organization.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import Any

from documentcloud import DocumentCloud

from lib.sources import env

DEFAULT_TIMEOUT = 900.0  # large filings (hundreds of pages) take minutes to process
IN_PROGRESS = frozenset({"pending", "readable", "nofile"})


class UploadError(RuntimeError):
    """DocumentCloud could not process the upload."""


@cache
def client() -> DocumentCloud:
    """Authenticated client (credentials from ``.env``)."""
    env.require(*env.VARIABLES["documentcloud"])
    return DocumentCloud(env.get("DOCUMENTCLOUD_USERNAME"), env.get("DOCUMENTCLOUD_PASSWORD"))


def _data_values(doc: Any, key: str) -> list[str]:
    data = getattr(doc, "data", None) or {}
    value = data.get(key) or []
    return [value] if isinstance(value, str) else list(value)


def find_by_citekey(citekey: str) -> Any | None:
    """The document tagged ``citekey`` in DocumentCloud's data, if one was uploaded."""
    for doc in client().documents.search(f'data_citekey:"{citekey}"'):
        if citekey in _data_values(doc, "citekey"):
            return doc
    return None


def project_id(title: str) -> int:
    """ID of the DocumentCloud project named ``title`` (created when missing)."""
    project, _ = client().projects.get_or_create_by_title(title)
    return project.id


def start_upload(
    path: Path,
    title: str,
    source: str,
    description: str,
    project: str | None,
    citekey: str,
    access: str = "public",
) -> int:
    """Upload ``path`` and return the DocumentCloud ID as soon as processing has started."""
    kwargs: dict[str, Any] = {
        "title": title,
        "source": source,
        "description": description,
        "access": access,
        "data": {"citekey": [citekey]},
    }
    if project:
        kwargs["project"] = project_id(project)
    doc = client().documents.upload(str(path), **kwargs)
    return int(doc.id)


def wait_until_ready(
    doc_id: int,
    timeout: float = DEFAULT_TIMEOUT,
    poll_seconds: float = 5.0,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Poll until the document is processed and public; return its canonical URL.

    Raises :class:`UploadError` when processing fails, so the caller can re-upload.
    """
    deadline = time.monotonic() + timeout
    while True:
        doc = client().documents.get(doc_id)
        if doc.status == "success":
            if doc.access != "public":
                doc.access = "public"
                doc.save()
            return str(doc.canonical_url)
        if doc.status == "error":
            raise UploadError(f"DocumentCloud failed to process document {doc_id}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"DocumentCloud document {doc_id} still {doc.status!r} after {timeout:.0f}s")
        sleep(poll_seconds)


def upload(
    path: Path,
    title: str,
    source: str,
    description: str,
    project: str | None,
    citekey: str,
    access: str = "public",
) -> tuple[int, str]:
    """Upload, wait for processing, and return ``(id, canonical_url)``."""
    doc_id = start_upload(path, title, source, description, project, citekey, access)
    return doc_id, wait_until_ready(doc_id)


def delete(doc_id: int) -> None:
    """Remove a failed upload so it can be retried."""
    client().documents.delete(doc_id)


def whoami() -> dict[str, Any]:
    """Account, organization and whether the organization is verified (needed to publish publicly)."""
    c = client()
    user = c.users.get(c.user_id)
    org = user.organization
    if isinstance(org, int):  # the users endpoint returns the organization as a bare ID
        org = c.organizations.get(org)
    return {
        "user": getattr(user, "name", None),
        "organization": getattr(org, "name", None),
        "verified": getattr(org, "verified_journalist", None),
    }
