"""``just sources-doctor``: is everything the pipeline needs set up and working?

One result per check with a fix hint. Credentials are never printed. Every check is read-only: the ``pub``
push check is ``git push --dry-run``.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from lib.sources import env

OK, WARN, FAIL = "ok", "warn", "fail"


@dataclass(frozen=True)
class Check:
    name: str
    level: str
    detail: str = ""
    hint: str = ""

    def line(self) -> str:
        mark = {"ok": "PASS", "warn": "WARN", "fail": "FAIL"}[self.level]
        text = f"[{mark}] {self.name}" + (f": {self.detail}" if self.detail else "")
        return text + (f"\n       fix: {self.hint}" if self.hint and self.level != OK else "")


def _guard(name: str, fn: Callable[[], Check], hint: str) -> Check:
    try:
        return fn()
    except Exception as e:  # a failed check is a result, not a crash
        return Check(name, FAIL, f"{type(e).__name__}: {e}"[:300], hint)


def check_env() -> list[Check]:
    out = []
    hints = {
        "zotero": "create a Zotero API key with write and file access (https://www.zotero.org/settings/keys) and set it in .env",
        "documentcloud": "use the shared DocumentCloud login from the password manager",
        "gdrive": "set the ID of the public folder in the shared drive (see context/code/sources_user_guide.md)",
        "google_oauth": "copy the G_* OAuth app variables from the team password manager (same ones lib/data/gsheets.py uses)",
        "wayback": "create archive.org S3-style keys at https://archive.org/account/s3.php (without them, capture falls back to the slower legacy anonymous endpoint)",
        "contact": "set a monitored e-mail (Crossref and Unpaywall polite pools)",
    }
    for service, names in env.VARIABLES.items():
        for name in names:
            level = OK if env.get(name) else (WARN if service in ("wayback", "contact") else FAIL)
            out.append(Check(f"{name} set", level, "" if level == OK else "not set", hints[service]))
    return out


def check_zotero() -> list[Check]:
    from lib.sources import zotero

    hint = "check ZOTERO_API_KEY / ZOTERO_GROUP_ID in .env"

    def access() -> Check:
        info = zotero.client().key_info().get("access", {})
        groups = info.get("groups", {})
        gid = env.get("ZOTERO_GROUP_ID") or ""
        perms = groups.get(gid) or groups.get("all") or {}
        if not perms:
            return Check(
                "Zotero key sees the group library", FAIL, "no access to this group", "give the key access to the group"
            )
        if not perms.get("write"):
            return Check("Zotero key can write", FAIL, "read-only key", "recreate the key with 'Allow write access'")
        return Check("Zotero key can write", OK, "group library read/write")

    def tree() -> Check:
        cols = zotero.collections()
        names = {c["data"]["name"] for c in cols if not c["data"]["parentCollection"]}
        if zotero.REPORTS not in names:
            return Check("Zotero 'Reports' collection", FAIL, "missing", "create a top-level collection named Reports")
        return Check("Zotero 'Reports' collection", OK, f"{len(zotero.project_collections(cols))} projects")

    def inbox() -> Check:
        if zotero.inbox_key() is None:
            return Check(
                "Zotero 'Inbox' collection",
                WARN,
                "missing (new items cannot be triaged by collection)",
                "create a top-level collection named Inbox",
            )
        return Check("Zotero 'Inbox' collection", OK)

    return [
        _guard("Zotero key", access, hint),
        _guard("Zotero Reports", tree, hint),
        _guard("Zotero Inbox", inbox, hint),
    ]


def check_documentcloud() -> list[Check]:
    from lib.sources import documentcloud

    def run() -> Check:
        who: dict[str, Any] = documentcloud.whoami()
        if not who.get("verified"):
            return Check(
                "DocumentCloud login",
                WARN,
                f"{who.get('user')} ({who.get('organization')}): organization is not verified, public uploads may be refused",
                "ask DocumentCloud support to verify the organization",
            )
        return Check("DocumentCloud login", OK, f"{who.get('user')} ({who.get('organization')})")

    return [_guard("DocumentCloud login", run, "check DOCUMENTCLOUD_USERNAME / DOCUMENTCLOUD_PASSWORD")]


def check_gdrive() -> list[Check]:
    """Google login checks: cached token present, scopes include Drive, token refreshable, folder reachable."""
    from lib.data import gsheets
    from lib.sources import gdrive

    login_hint = "run `just google-login` once (on a laptop if this machine has no browser, then copy the token file)"
    out: list[Check] = []
    token = gsheets.load_cached_token()
    token_path = gsheets._gspread_token_path()
    if token is None:
        return [Check("Google login token cached", FAIL, f"no token at {token_path}", login_hint)]
    out.append(Check("Google login token cached", OK, str(token_path)))
    scopes = set(token.get("scopes") or [])
    has_drive = gdrive.SCOPES[0] in scopes
    out.append(
        Check(
            "Google token has Drive scope",
            OK if has_drive else FAIL,
            "" if has_drive else f"granted: {sorted(scopes) or 'none recorded'}",
            "delete the token file and run `just google-login` (the login asks for Drive access)",
        )
    )

    def refresh() -> Check:
        gsheets.get_user_credentials(gdrive.SCOPES)
        return Check("Google token refreshable", OK, str(token.get("account") or ""))

    refreshed = _guard(
        "Google token refreshable",
        refresh,
        "tokens expire after 7 days when the OAuth consent screen is External+Testing; run `just google-login` again",
    )
    out.append(refreshed)
    if refreshed.level != OK or not env.get("GDRIVE_PUBLIC_FOLDER_ID"):
        return out

    def folder() -> Check:
        who = gdrive.whoami()
        where = "shared drive" if who.get("shared_drive") else "NOT in a shared drive (files would belong to you)"
        return Check(
            "Google Drive public folder", OK if who.get("shared_drive") else WARN, f"{who.get('folder')} ({where})"
        )

    out.append(
        _guard(
            "Google Drive public folder",
            folder,
            "check GDRIVE_PUBLIC_FOLDER_ID, and that your Google account is a member of the shared drive",
        )
    )
    return out


def check_tools() -> list[Check]:
    out = []
    for tool, why in (("quarto", "sync-bib needs it"), ("yamlfmt", "sync-bib needs it")):
        path = shutil.which(tool)
        out.append(Check(f"{tool} on PATH", OK if path else FAIL, why if not path else "", f"install {tool}"))

    def chromium() -> Check:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            exe = p.chromium.executable_path
        from pathlib import Path

        return Check(
            "Playwright Chromium",
            OK if Path(exe).exists() else FAIL,
            "" if Path(exe).exists() else "not installed",
            "uv run playwright install chromium",
        )

    out.append(_guard("Playwright Chromium", chromium, "uv run playwright install chromium"))
    return out


def check_pub() -> list[Check]:
    from lib.sources import shortlinks

    def run() -> Check:
        repo = shortlinks.ensure_clone()
        result = subprocess.run(["git", "-C", str(repo), "push", "--dry-run"], capture_output=True, text=True)
        if result.returncode != 0:
            return Check(
                "switchbox-data/pub push access",
                FAIL,
                result.stderr.strip()[-200:],
                "gh auth login (needs write access to switchbox-data/pub)",
            )
        return Check("switchbox-data/pub push access", OK, str(repo))

    return [_guard("switchbox-data/pub push access", run, "gh auth login (needs write access to switchbox-data/pub)")]


def run_all() -> list[Check]:
    checks = check_env()
    if env.get("ZOTERO_API_KEY"):
        checks += check_zotero()
    if env.get("DOCUMENTCLOUD_USERNAME") and env.get("DOCUMENTCLOUD_PASSWORD"):
        checks += check_documentcloud()
    if env.get("G_CLIENT_ID"):
        checks += check_gdrive()
    checks += check_tools() + check_pub()
    return checks
