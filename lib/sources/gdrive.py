"""Public hosting of Excel workbooks (and, while DocumentCloud is unavailable, PDFs) on a Google shared drive.

Uses Drive API v3 with the teammate's Google login. Files are uploaded unconverted to ``<GDRIVE_PUBLIC_FOLDER_ID>/<project>/`` and shared as "anyone with the
link can view". Each file carries ``appProperties`` (``citekey``, ``md5``) so a rerun finds an existing upload
instead of creating a second one. Drive's md5 is compared with the local file's before a copy is trusted.

Auth is the user OAuth login that ``lib.data.gsheets`` already caches (``just google-login`` once); uploads run
as whoever runs ingest, and because the folder is on a shared drive the files belong to the shared drive.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from lib.sources import env

SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME = "application/vnd.google-apps.folder"
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
PDF_MIME = "application/pdf"
_LIST_ARGS = {"supportsAllDrives": True, "includeItemsFromAllDrives": True, "corpora": "allDrives"}


@dataclass(frozen=True)
class DriveFile:
    """A file on the public shared drive."""

    id: str
    url: str
    md5: str | None


def view_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"


@cache
def service() -> Any:
    """Drive v3 service using the cached Google user login (see :func:`lib.data.gsheets.get_user_credentials`)."""
    from googleapiclient.discovery import build

    from lib.data import gsheets

    return build("drive", "v3", credentials=gsheets.get_user_credentials(SCOPES), cache_discovery=False)


def _q(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _first(query: str, fields: str = "files(id, name, md5Checksum)") -> dict[str, Any] | None:
    files = service().files().list(q=query, fields=fields, pageSize=10, **_LIST_ARGS).execute().get("files", [])
    return files[0] if files else None


def ensure_folder(name: str, parent_id: str) -> str:
    """ID of the folder ``name`` under ``parent_id`` (created when missing)."""
    found = _first(
        f"name = '{_q(name)}' and '{_q(parent_id)}' in parents and mimeType = '{FOLDER_MIME}' and trashed = false"
    )
    if found:
        return found["id"]
    body = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]}
    return service().files().create(body=body, fields="id", supportsAllDrives=True).execute()["id"]


def find_existing(citekey: str, file_id: str | None = None) -> DriveFile | None:
    """The file already uploaded for ``citekey`` (by recorded file ID, else by ``appProperties``)."""
    if file_id:
        f = service().files().get(fileId=file_id, fields="id, md5Checksum, trashed", supportsAllDrives=True).execute()
        if not f.get("trashed"):
            return DriveFile(f["id"], view_url(f["id"]), f.get("md5Checksum"))
    found = _first(f"appProperties has {{ key='citekey' and value='{_q(citekey)}' }} and trashed = false")
    return DriveFile(found["id"], view_url(found["id"]), found.get("md5Checksum")) if found else None


def share_publicly(file_id: str) -> None:
    """Anyone with the link can view (not listed in search)."""
    body = {"type": "anyone", "role": "reader", "allowFileDiscovery": False}
    service().permissions().create(fileId=file_id, body=body, supportsAllDrives=True).execute()


def is_public(file_id: str) -> bool:
    perms = (
        service().permissions().list(fileId=file_id, fields="permissions(type, role)", supportsAllDrives=True).execute()
    )
    return any(p.get("type") == "anyone" for p in perms.get("permissions", []))


def upload(path: Path, project: str, citekey: str, md5: str, file_id: str | None = None) -> DriveFile:
    """Upload ``path`` to ``<root>/<project>/``, share it publicly and verify Drive's md5 equals ``md5``.

    Reuses an existing upload for ``citekey`` (checking its md5 and sharing); never creates a second copy.
    """
    from googleapiclient.http import MediaFileUpload

    existing = find_existing(citekey, file_id)
    if existing is None:
        root = env.get("GDRIVE_PUBLIC_FOLDER_ID")
        if not root:
            raise RuntimeError("Set GDRIVE_PUBLIC_FOLDER_ID in .env")
        parent = ensure_folder(project, root)
        body = {"name": Path(path).name, "parents": [parent], "appProperties": {"citekey": citekey, "md5": md5}}
        mime = PDF_MIME if Path(path).suffix.lower() == ".pdf" else XLSX_MIME
        media = MediaFileUpload(str(path), mimetype=mime, resumable=True)
        created = (
            service()
            .files()
            .create(body=body, media_body=media, fields="id, md5Checksum", supportsAllDrives=True)
            .execute()
        )
        existing = DriveFile(created["id"], view_url(created["id"]), created.get("md5Checksum"))
    if existing.md5 and existing.md5 != md5:
        raise RuntimeError(f"Drive file {existing.id} has md5 {existing.md5}, expected {md5}")
    if not is_public(existing.id):
        share_publicly(existing.id)
    return existing


def whoami() -> dict[str, Any]:
    """The signed-in account and whether it can see the public folder, for ``doctor``."""
    env.require("GDRIVE_PUBLIC_FOLDER_ID")
    root = env.get("GDRIVE_PUBLIC_FOLDER_ID") or ""
    f = service().files().get(fileId=root, fields="id, name, mimeType, driveId", supportsAllDrives=True).execute()
    return {"folder": f.get("name"), "id": f.get("id"), "shared_drive": bool(f.get("driveId"))}
