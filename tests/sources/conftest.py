"""Shared fixtures for the source-ingest tests: an in-memory Zotero, DocumentCloud and Drive, and a local ``pub`` remote.

Nothing here touches the network. ``World`` replaces the module-level functions the ingest orchestrator calls, so
a test can make any one of them fail and check that rerunning the same card finishes the job without duplicates.
"""

from __future__ import annotations

import copy
import json
import subprocess
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from lib.sources import (
    citekeys,
    documentcloud,
    env,
    extra,
    gdrive,
    metadata,
    shortlinks,
    webpage,
    zotero,
)

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.org",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.org",
    "GIT_TERMINAL_PROMPT": "0",
}


def _git(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture(autouse=True)
def pdf_host_documentcloud(monkeypatch: pytest.MonkeyPatch) -> None:
    """Most tests exercise the DocumentCloud path; Drive-hosted PDFs are tested by setting the host explicitly."""
    monkeypatch.setenv("SOURCES_PDF_HOST", "documentcloud")


@pytest.fixture
def cache_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "cache"
    monkeypatch.setenv("SOURCES_CACHE_DIR", str(path))
    for name, value in GIT_ENV.items():
        monkeypatch.setenv(name, value)
    return path


@pytest.fixture
def pub_remote(tmp_path: Path, cache_dir: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A bare git repo seeded like switchbox-data/pub, used as the short-link remote."""
    bare = tmp_path / "pub.git"
    seed = tmp_path / "seed"
    _git("init", "--bare", "-b", "main", str(bare))
    _git("init", "-b", "main", str(seed))
    (seed / "CNAME").write_text("pub.switch.box\n")
    shortlinks.save_links(seed, {"test": "https://switch.box/"})
    _git("add", ".", cwd=seed)
    _git("commit", "-m", "seed", cwd=seed)
    _git("remote", "add", "origin", str(bare), cwd=seed)
    _git("push", "-u", "origin", "main", cwd=seed)
    monkeypatch.setenv("SOURCES_PUB_REMOTE", str(bare))
    return bare


def remote_links(bare: Path, tmp_path: Path) -> dict[str, str]:
    """links.json as currently on the remote."""
    out = subprocess.run(
        ["git", "--git-dir", str(bare), "show", "main:links.json"], capture_output=True, text=True, check=True
    )
    return json.loads(out.stdout)


def remote_commits(bare: Path) -> int:
    out = subprocess.run(
        ["git", "--git-dir", str(bare), "rev-list", "--count", "main"], capture_output=True, text=True, check=True
    )
    return int(out.stdout.strip())


class World:
    """In-memory Zotero library, DocumentCloud, Drive and Wayback, with injectable failures."""

    def __init__(self) -> None:
        self.items: dict[str, dict[str, Any]] = {}
        self.children: dict[str, list[dict[str, Any]]] = {}
        self.files: dict[str, bytes] = {}
        self.tokens: dict[str, str] = {}
        self.calls: Counter[str] = Counter()
        self.failures: dict[str, list[Exception]] = {}
        self.dc: dict[int, dict[str, Any]] = {}
        self.drive: dict[str, gdrive.DriveFile] = {}
        self.collections = {"ma_hp_rates": "COL_MA", "ri_hp_rates": "COL_RI"}
        self.inbox: str | None = "COL_INBOX"
        self.next_key = 0
        self.next_dc = 100
        self.wayback_blocked = False

    # --- helpers ---------------------------------------------------------------------------------

    def fail_next(self, name: str, error: Exception | None = None, times: int = 1) -> None:
        self.failures[name] = [error or RuntimeError(f"injected failure in {name}") for _ in range(times)]

    def _call(self, name: str) -> None:
        self.calls[name] += 1
        if self.failures.get(name):
            raise self.failures[name].pop(0)

    def _new_key(self) -> str:
        self.next_key += 1
        return f"ITEM{self.next_key:04d}"

    def add_item(self, data: dict[str, Any]) -> str:
        key = self._new_key()
        data = {"tags": [], "collections": [], "extra": "", "relations": {}, **data}
        data["dateAdded"] = "2026-10-28T10:00:00Z"
        self.items[key] = {"key": key, "version": 1, "data": data}
        self.children[key] = []
        return key

    def library(self) -> list[dict[str, Any]]:
        out = [copy.deepcopy(it) for it in self.items.values()]
        for parent, kids in self.children.items():
            out += [{"key": k["key"], "version": 1, "data": {**k, "parentItem": parent}} for k in kids]
        return out

    def attachments_of(self, key: str) -> list[dict[str, Any]]:
        return self.children[key]

    # --- zotero ------------------------------------------------------------------------------------

    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        w = self

        def pinned_keys() -> dict[str, str]:
            return {
                k: it["key"] for it in w.items.values() if (k := extra.get(it["data"].get("extra"), extra.CITATION_KEY))
            }

        def get_item(key: str) -> dict[str, Any]:
            if key in w.items:
                return copy.deepcopy(w.items[key])
            for parent, kids in w.children.items():
                for kid in kids:
                    if kid["key"] == key:
                        return {"key": key, "version": 1, "data": {**copy.deepcopy(kid), "parentItem": parent}}
            raise KeyError(key)

        def create_item(data: dict[str, Any], write_token: str | None = None) -> str:
            w._call("create_item")
            if write_token and write_token in w.tokens:
                return w.tokens[write_token]
            key = w.add_item(dict(data))
            if write_token:
                w.tokens[write_token] = key
            return key

        def update_from_card(item_key: str, data: dict[str, Any], project_keys: list[str]) -> None:
            w._call("update_from_card")
            current = w.items[item_key]["data"]
            for k, v in data.items():
                if k not in ("extra", "collections", "tags", "relations"):
                    current[k] = v
            for name in (extra.CITATION_KEY, extra.SHORTAUTHOR):
                if value := extra.get(data.get("extra"), name):
                    current["extra"] = extra.set_field(current.get("extra"), name, value)
            current["collections"] = sorted({c for c in current["collections"] if c != w.inbox} | set(project_keys))

        def stored_attachments(item_key: str) -> list[dict[str, Any]]:
            return [{"key": c["key"], "data": c} for c in w.children[item_key] if c["linkMode"] == "imported_file"]

        def attach_file(item_key: str, path: Path, title: str | None = None) -> str:
            w._call("attach_file")
            md5 = zotero.file_md5(Path(path))
            for c in w.children[item_key]:
                if c.get("md5") == md5:
                    return c["key"]
            key = w._new_key()
            w.children[item_key].append(
                {
                    "key": key,
                    "itemType": "attachment",
                    "linkMode": "imported_file",
                    "md5": md5,
                    "filename": Path(path).name,
                    "title": title or Path(path).name,
                    "contentType": "application/pdf",
                }
            )
            w.files[key] = Path(path).read_bytes()
            return key

        def attach_link(item_key: str, url: str, title: str) -> str:
            w._call("attach_link")
            for c in w.children[item_key]:
                if c.get("url") == url:
                    return c["key"]
            key = w._new_key()
            w.children[item_key].append(
                {"key": key, "itemType": "attachment", "linkMode": "linked_url", "url": url, "title": title}
            )
            return key

        def set_extra_fields(item_key: str, fields: dict[str, str | None]) -> None:
            w._call("set_extra_fields")
            data = w.items[item_key]["data"]
            for name, value in fields.items():
                data["extra"] = extra.set_field(data.get("extra"), name, value)

        def mark_processed(item_key: str) -> None:
            w._call("mark_processed")
            tags = w.items[item_key]["data"]["tags"]
            if not any(t["tag"] == zotero.PROCESSED_TAG for t in tags):
                tags.append({"tag": zotero.PROCESSED_TAG})

        def download_attachment(item_key: str, dest_dir: Path) -> Path:
            w._call("download_attachment")
            att = next(c for c in w.children[item_key] if c["linkMode"] == "imported_file")
            dest_dir.mkdir(parents=True, exist_ok=True)
            path = dest_dir / att["filename"]
            path.write_bytes(w.files[att["key"]])
            return path

        def adopt_raw_file(attachment_key: str, parent_key: str) -> None:
            w._call("adopt_raw_file")
            raw = w.items.pop(attachment_key)
            w.children.pop(attachment_key, None)
            w.children[parent_key].append({**raw["data"], "key": attachment_key, "collections": []})

        real_find = zotero.find_duplicates

        def find_duplicates_fake(md5=None, url=None, doi=None, title=None, items=None):
            return real_find(md5=md5, url=url, doi=doi, title=title, items=w.library())

        patches = {
            "pinned_keys": pinned_keys,
            "get_item": get_item,
            "create_item": create_item,
            "update_from_card": update_from_card,
            "stored_attachments": stored_attachments,
            "attach_file": attach_file,
            "attach_link": attach_link,
            "set_extra_fields": set_extra_fields,
            "mark_processed": mark_processed,
            "download_attachment": download_attachment,
            "adopt_raw_file": adopt_raw_file,
            "find_duplicates": find_duplicates_fake,
            "project_collections": lambda cols=None: dict(w.collections),
            "inbox_key": lambda cols=None: w.inbox,
            "today": lambda: "2026-10-28",
        }
        for name, fn in patches.items():
            monkeypatch.setattr(zotero, name, fn)

        # DocumentCloud
        def dc_find(citekey: str) -> Any:
            for doc_id, doc in w.dc.items():
                if doc["citekey"] == citekey:
                    return SimpleNamespace(id=doc_id)
            return None

        def dc_start(
            path: Path,
            title: str,
            source: str,
            description: str,
            project: str | None,
            citekey: str,
            access: str = "public",
        ) -> int:
            w._call("dc_start_upload")
            w.next_dc += 1
            w.dc[w.next_dc] = {"citekey": citekey, "status": "success"}
            return w.next_dc

        def dc_wait(doc_id: int, **_: Any) -> str:
            w._call("dc_wait")
            doc = w.dc[doc_id]
            if doc["status"] == "error":
                raise documentcloud.UploadError(f"document {doc_id} failed")
            return f"https://www.documentcloud.org/documents/{doc_id}-{doc['citekey']}"

        monkeypatch.setattr(documentcloud, "find_by_citekey", dc_find)
        monkeypatch.setattr(documentcloud, "start_upload", dc_start)
        monkeypatch.setattr(documentcloud, "wait_until_ready", dc_wait)
        monkeypatch.setattr(documentcloud, "delete", lambda doc_id: w.dc.pop(doc_id, None))

        # Drive
        def drive_upload(
            path: Path, project: str, citekey: str, md5: str, file_id: str | None = None
        ) -> gdrive.DriveFile:
            w._call("drive_upload")
            if citekey not in w.drive:
                w.drive[citekey] = gdrive.DriveFile(
                    f"DRV{len(w.drive) + 1}", f"https://drive.google.com/file/d/DRV{len(w.drive) + 1}/view", md5
                )
            return w.drive[citekey]

        monkeypatch.setattr(gdrive, "upload", drive_upload)

        # Web
        def capture(url: str, out_dir: Path, stem: str, timeout_ms: int = 0) -> webpage.Capture:
            w._call("capture")
            out_dir.mkdir(parents=True, exist_ok=True)
            pdf, html = out_dir / f"{stem}.pdf", out_dir / f"{stem}.html"
            pdf.write_bytes(b"%PDF-1.4 fake capture")
            html.write_text("<html><body><nav>menu</nav><main><h1>Page</h1><p>Hello world.</p></main></body></html>")
            return webpage.Capture(url, url, "Page", "2026-10-28", pdf, html, zotero.file_md5(pdf))

        def wayback(url: str, **_: Any) -> webpage.WaybackResult:
            w._call("wayback")
            if w.wayback_blocked:
                return webpage.WaybackResult(False, None, True, "blocked")
            return webpage.WaybackResult(True, f"https://web.archive.org/web/20261028000000/{url}", False, "")

        monkeypatch.setattr(webpage, "capture", capture)
        monkeypatch.setattr(webpage, "wayback_save", wayback)


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch, cache_dir: Path, pub_remote: Path) -> World:
    w = World()
    w.install(monkeypatch)
    monkeypatch.setenv("ZOTERO_GROUP_ID", "999")
    return w


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A miniature reports2 checkout: ``context/README.md`` with a sources table, and a project folder."""
    root = tmp_path / "repo"
    (root / "context" / "sources" / "ma_hp_rates").mkdir(parents=True)
    (root / "context" / "README.md").write_text(
        "# Context index\n\n## sources/\n\nPrimary sources.\n\n"
        "| File | Use when working on … |\n| ---- | ---- |\n"
        "| `bonbright_1960/` (directory) | Bonbright. |\n"
        "| ma_hp_rates/older.md | Older document. |\n\n## code/\n\nCode notes.\n",
        encoding="utf-8",
    )
    return root


def make_card(**overrides: Any) -> metadata.SourceMetadata:
    """A valid card for a Massachusetts DPU order, with the rule's citation key filled in."""
    base: dict[str, Any] = {
        "citekey": "placeholder",
        "item_type": "document",
        "title": "Docket 25-55: Order on Seasonal Heat Pump Rates",
        "creators": [{"name": "Massachusetts Department of Public Utilities"}],
        "abbreviation": "MA DPU",
        "date": "2025-06-01",
        "docket": "25-55",
        "projects": ["ma_hp_rates"],
        "source_file": "order.pdf",
        "source_url": "https://example.org/files/order.pdf",
        "extract_path": "context/sources/ma_hp_rates/madpu_25-55_order.md",
        "index_row": "DPU order on seasonal heat pump rates; read for the approved design.",
        "front_matter": {"docket": "25-55", "pages_total": 12, "extraction_scope": "full"},
    }
    base.update(overrides)
    draft = metadata.SourceMetadata.model_validate(base)
    key = overrides.get("citekey") or citekeys.propose_key(draft.zotero_data(), set())
    return draft.model_copy(update={"citekey": key})


EXTRACT_TEXT = """---
source: order.pdf
docket: 25-55  # as printed on every page
utility: National Grid
original_pdf_path: /staging/order.pdf
why_here: Approved design.
---

# Order

Body text.
"""


@pytest.fixture
def pdf_file(tmp_path: Path) -> Path:
    path = tmp_path / "order.pdf"
    path.write_bytes(b"%PDF-1.4 original order\n")
    return path


@pytest.fixture
def extract_file(repo: Path) -> Path:
    path = repo / "context" / "sources" / "ma_hp_rates" / "madpu_25-55_order.md"
    path.write_text(EXTRACT_TEXT, encoding="utf-8")
    return path


def use_repo_env(monkeypatch: pytest.MonkeyPatch, repo: Path) -> None:
    monkeypatch.setattr(env, "REPO_ROOT", repo)
    monkeypatch.setattr(env, "SOURCES_DIR", repo / "context" / "sources")
