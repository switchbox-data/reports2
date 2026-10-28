"""Ingest one approved source card into Zotero, the public hosts, the short-link map and the repo.

"The agent decides, the CLI does": the card (``metadata.SourceMetadata``) holds every judgment; this module
performs the writes, in an order that makes any failure safe to rerun. Each step first looks at the real
system -- the Zotero item with this pinned key, the DocumentCloud ID in its Extra (or a document tagged with
the key), attachments with the same md5, the link already in ``links.json``, front-matter fields already
written, index rows already present -- and does only what is missing. Nothing is tracked in a local state
file; the systems themselves are the state.

The ``processed`` tag goes on last, after every step has been verified. Items without it show up in
``just sources-pending``.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from rapidfuzz import fuzz

from lib.sources import (
    documentcloud,
    env,
    extra,
    frontmatter,
    gdrive,
    indexes,
    metadata,
    projects,
    shortlinks,
    webpage,
    workbook,
    zotero,
)

CAPTURE_TITLE = "Web capture (PDF)"
DOCUMENTCLOUD_TITLE = "Public copy (DocumentCloud)"
DRIVE_TITLE = "Public copy (Google Drive)"
WAYBACK_TITLE = "Wayback Machine capture"
ORIGINAL_TITLE = "Original source"

SAME_TITLE = 90  # similarity (0-100) of titles that identifies a rerun of the same card


def _norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


DONE, ALREADY, SKIPPED, PENDING, FAILED = "done", "already", "skipped", "pending", "failed"


class IngestError(RuntimeError):
    """A step failed in a way the person should read (a duplicate, an unknown project, ...)."""


@dataclass
class Step:
    name: str
    status: str
    detail: str = ""


@dataclass
class IngestReport:
    """What happened, per step, plus the links the person needs."""

    citekey: str
    steps: list[Step] = field(default_factory=list)
    item_key: str | None = None
    zotero_web: str | None = None
    zotero_desktop: str | None = None
    public_url: str | None = None
    short_url: str | None = None
    processed: bool = False
    notes: list[str] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "") -> Step:
        step = Step(name, status, detail)
        self.steps.append(step)
        return step

    @property
    def failed(self) -> list[Step]:
        return [s for s in self.steps if s.status == FAILED]

    @property
    def pending(self) -> list[Step]:
        return [s for s in self.steps if s.status == PENDING]

    @property
    def ok(self) -> bool:
        return not self.failed and not self.pending

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "ok": self.ok}


def write_token(citekey: str) -> str:
    """Zotero write token for creating this key's item: a repeated create is rejected, not duplicated."""
    return hashlib.sha256(f"switchbox-source-{citekey}".encode()).hexdigest()[:32]


def save_card(meta: metadata.SourceMetadata) -> Path:
    """Keep the approved card in the scratch folder so a failed ingest can be rerun from it."""
    path = env.cache_dir() / "cards" / f"{meta.citekey}.yaml"
    metadata.dump(meta, path)
    return path


class Ingest:
    """One document's ingest. ``run`` executes the steps; ``finalize`` verifies and tags it processed."""

    def __init__(
        self,
        meta: metadata.SourceMetadata,
        source: Path | None = None,
        zotero_item: str | None = None,
        extract: Path | None = None,
        links: shortlinks.Batch | None = None,
        force: bool = False,
        scratch: Path | None = None,
        repo_root: Path | None = None,
    ):
        self.meta = meta
        self.source = Path(source) if source else None
        self.zotero_item = zotero_item
        self.extract = Path(extract) if extract else None
        self.links = links
        self.force = force
        self.scratch = Path(scratch) if scratch else env.cache_dir() / "downloads"
        self.repo_root = Path(repo_root) if repo_root else env.REPO_ROOT
        self.report = IngestReport(meta.citekey)
        self.item_key: str | None = None
        self.md5: str | None = None
        self.capture: webpage.Capture | None = None
        self._local: Path | None = self.source
        self._dc_id: int | None = None
        self.raw_file: str | None = None

    # --- plumbing ---------------------------------------------------------------------------------

    def _step(self, name: str, fn: Any) -> bool:
        """Run ``fn() -> (status, detail)``; a raised error becomes a failed step. True when it did not fail."""
        try:
            status, detail = fn()
        except Exception as e:  # report and continue; every step is rerunnable
            self.report.add(name, FAILED, f"{type(e).__name__}: {e}")
            return False
        self.report.add(name, status, detail)
        return True

    def _item_extra(self) -> str:
        assert self.item_key
        return zotero.get_item(self.item_key)["data"].get("extra") or ""

    def local_file(self) -> Path:
        """The original file on disk, downloaded from the Zotero item when this run was not given one."""
        if self._local is None:
            assert self.item_key
            self._local = zotero.download_attachment(self.item_key, self.scratch / self.meta.citekey)
        return self._local

    @property
    def extract_path(self) -> Path | None:
        if self.extract:
            return self.extract
        return self.repo_root / self.meta.extract_path if self.meta.extract_path else None

    # --- steps --------------------------------------------------------------------------------------

    def validate(self) -> tuple[str, str]:
        taken = zotero.pinned_keys()
        own = taken.get(self.meta.citekey)
        if self.zotero_item:
            self.zotero_item = self._resolve_zotero_item(self.zotero_item)
        if self.zotero_item:
            if own and own != self.zotero_item:
                raise IngestError(f"citekey {self.meta.citekey} already belongs to Zotero item {own}")
            self.item_key = self.zotero_item
        else:
            self.item_key = own
            if own and not self._same_document(own):
                self.item_key = None  # a different document pinned this key: report the collision below
        if own and own == self.item_key:
            taken.pop(self.meta.citekey)
        problems = self.meta.problems(set(taken))
        known = zotero.project_collections()
        for p in self.meta.projects:
            if p not in known and not self.meta.new_project:
                problems.append(f"no Reports subcollection {p!r}; set new_project: true to create it")
        src = self.source
        if src and self.meta.is_workbook and workbook.needs_decision(src, self.meta.workbook_in_repo):
            problems.append("workbook is over the 600 KB repo limit: set workbook_in_repo to true or false")
        if self.meta.extract_path and not self.meta.index_row:
            problems.append("a card with extract_path needs index_row (one sentence for context/README.md)")
        if problems:
            raise metadata.MetadataError(problems)
        return DONE, "card valid" + (f"; resuming item {self.item_key}" if self.item_key else "")

    def _resolve_zotero_item(self, key: str) -> str | None:
        """The item to adopt for ``--zotero-item key``; ``None`` when ``key`` is a raw file still needing an item.

        A file already moved under an item (by an earlier run) resolves to that item. A raw file is remembered in
        ``raw_file``, and ``ensure_item`` moves it under the item it creates (or the one pinned to this citekey).
        """
        data = zotero.get_item(key)["data"]
        if data["itemType"] != "attachment":
            return key
        if data.get("parentItem"):
            return data["parentItem"]
        if not zotero.is_raw_file(data):
            raise IngestError(f"Zotero attachment {key} is a link, not a stored file; attach the file in Zotero")
        self.raw_file = key
        return None

    def _same_document(self, item_key: str) -> bool:
        """Whether the item already pinned to this key is this card's document (a rerun), not a collision."""
        have = zotero.get_item(item_key)["data"].get("title") or ""
        return fuzz.ratio(_norm(have), _norm(self.meta.title)) >= SAME_TITLE

    def new_projects(self) -> tuple[str, str]:
        known = zotero.project_collections()
        created = [p for p in self.meta.projects if p not in known]
        for p in created:
            projects.ensure_project(p)
        return (DONE, f"created {', '.join(created)}") if created else (SKIPPED, "")

    def resolve_file(self) -> tuple[str, str]:
        if self.source:
            self.md5 = zotero.file_md5(self.source)
            return DONE, f"md5 {self.md5}"
        if self.meta.is_web_page:
            return SKIPPED, "web page: captured after the item exists"
        return SKIPPED, "no local file; using the Zotero attachment"

    def ensure_item(self) -> tuple[str, str]:
        status, detail = self._ensure_item()
        if self.raw_file:
            assert self.item_key
            zotero.adopt_raw_file(self.raw_file, self.item_key)
            return DONE, f"{detail}; moved file {self.raw_file} under it"
        return status, detail

    def _ensure_item(self) -> tuple[str, str]:
        cols = zotero.project_collections()
        keys = [cols[p] for p in self.meta.projects]
        data = self.meta.zotero_data(keys)
        if self.item_key is None:
            if not self.force:
                dups = zotero.find_duplicates(
                    md5=self.md5, url=self.meta.source_url, doi=self.meta.doi, title=self.meta.title
                )
                if dups:
                    listing = "; ".join(f"{d.kind}: {d.item_key} {d.citekey or ''} {d.title[:50]}" for d in dups)
                    raise IngestError(f"possible duplicates ({listing}). Rerun with --zotero-item KEY to adopt one")
            self.item_key = zotero.create_item(data, write_token=write_token(self.meta.citekey))
            return DONE, f"created {self.item_key}"
        current = zotero.get_item(self.item_key)["data"]
        if self.zotero_item and extra.get(current.get("extra"), extra.CITATION_KEY) != self.meta.citekey:
            zotero.update_from_card(self.item_key, data, keys)
            return DONE, f"updated {self.item_key} from the card"
        return ALREADY, f"item {self.item_key}"

    def capture_page(self) -> tuple[str, str]:
        assert self.item_key
        if any(c["data"].get("title") == CAPTURE_TITLE for c in zotero.stored_attachments(self.item_key)):
            return ALREADY, "capture already attached"
        assert self.meta.source_url
        self.capture = webpage.capture(self.meta.source_url, self.scratch / self.meta.citekey, self.meta.citekey)
        self._local = self.capture.pdf_path
        self.md5 = self.capture.pdf_md5
        return DONE, f"captured {self.capture.final_url}"

    def attach_original(self) -> tuple[str, str]:
        assert self.item_key
        parts: list[str] = []
        if self._local is not None and (self.source or self.capture):
            title = CAPTURE_TITLE if self.capture else self._local.name
            zotero.attach_file(self.item_key, self._local, title=title)
            parts.append("file")
        if self.meta.source_url:
            zotero.attach_link(self.item_key, self.meta.source_url, ORIGINAL_TITLE)
            parts.append("original-source link")
        return (DONE, " + ".join(parts)) if parts else (SKIPPED, "nothing to attach")

    def documentcloud_start(self) -> tuple[str, str]:
        meta = self.meta
        if not meta.should_upload_documentcloud:
            return SKIPPED, "not uploaded (DOI, web page, or card says no)"
        assert self.item_key
        known = extra.get(self._item_extra(), zotero.DOCUMENTCLOUD_ID)
        if known:
            self._dc_id = int(known)
            return ALREADY, f"DocumentCloud {known}"
        found = documentcloud.find_by_citekey(meta.citekey)
        if found is None:
            self._dc_id = self._upload_dc()
            return DONE, f"uploaded as {self._dc_id}"
        self._dc_id = int(found.id)
        zotero.set_extra_fields(self.item_key, {zotero.DOCUMENTCLOUD_ID: str(self._dc_id)})
        return ALREADY, f"found DocumentCloud {self._dc_id} by citekey"

    def _upload_dc(self) -> int:
        assert self.item_key
        meta = self.meta
        project = meta.projects[0] if meta.projects else None
        path = self.local_file()
        author = ", ".join(c.name or f"{c.first_name} {c.last_name}" for c in meta.creators)
        dc_id = documentcloud.start_upload(path, meta.title, author, meta.title, project, meta.citekey)
        zotero.set_extra_fields(self.item_key, {zotero.DOCUMENTCLOUD_ID: str(dc_id)})
        return dc_id

    def documentcloud_ready(self) -> tuple[str, str]:
        if self._dc_id is None:
            return SKIPPED, ""
        assert self.item_key
        try:
            url = documentcloud.wait_until_ready(self._dc_id)
        except documentcloud.UploadError:
            documentcloud.delete(self._dc_id)
            self._dc_id = self._upload_dc()
            url = documentcloud.wait_until_ready(self._dc_id)
        self.meta.documentcloud_url = url
        zotero.attach_link(self.item_key, url, DOCUMENTCLOUD_TITLE)
        return DONE, url

    def drive(self) -> tuple[str, str]:
        meta = self.meta
        if not meta.is_workbook:
            return SKIPPED, "not a workbook"
        assert self.item_key
        known = extra.get(self._item_extra(), zotero.DRIVE_ID)
        path = self.local_file()
        md5 = self.md5 or zotero.file_md5(path)
        project = meta.projects[0]
        result = gdrive.upload(path, project, meta.citekey, md5, file_id=known)
        if known != result.id:
            zotero.set_extra_fields(self.item_key, {zotero.DRIVE_ID: result.id})
        meta.drive_url = result.url
        zotero.attach_link(self.item_key, result.url, DRIVE_TITLE)
        return (ALREADY if known else DONE), result.url

    def wayback(self) -> tuple[str, str]:
        meta = self.meta
        if not meta.is_web_page:
            return SKIPPED, "not a web page"
        assert self.item_key and meta.source_url
        known = extra.get(self._item_extra(), zotero.WAYBACK_URL)
        if known:
            meta.wayback_url = known
            return ALREADY, known
        result = webpage.wayback_save(meta.source_url)
        if result.blocked:
            self.report.notes.append(
                f"Wayback is blocked for {meta.source_url}: the short link points to the live page; the PDF capture is in Zotero"
            )
            return SKIPPED, "blocked by the site"
        if not result.ok or not result.url:
            raise IngestError(f"Wayback save failed: {result.message}")
        zotero.set_extra_fields(self.item_key, {zotero.WAYBACK_URL: result.url})
        zotero.attach_link(self.item_key, result.url, WAYBACK_TITLE)
        meta.wayback_url = result.url
        return DONE, result.url

    def short_link(self) -> tuple[str, str]:
        meta = self.meta
        if meta.doi:
            return SKIPPED, "DOI item: Zotero's url is the doi.org link"
        target = meta.short_link_target
        if target is None:
            raise IngestError("no public copy and no source_url: nothing for the short link to forward to")
        if self.links is None:
            raise IngestError("no short-link batch supplied")
        have = self.links.get(meta.citekey)
        if have == target:
            return ALREADY, f"{meta.short_url} -> {target}"
        if have is None:
            self.links.add(meta.citekey, target)
            return PENDING, f"queued {meta.short_url} -> {target} (published with the batch)"
        self.links.repoint(meta.citekey, target)
        return PENDING, f"queued repoint {meta.short_url} -> {target} (was {have})"

    def front_matter(self) -> tuple[str, str]:
        meta = self.meta
        path = self.extract_path
        if path is None:
            return SKIPPED, "card has no extract_path"
        ids: dict[str, Any] = {
            "source_file": meta.source_file,
            "citekey": meta.citekey,
            "zotero_item": self.item_key,
            "public_url": meta.public_url if meta.public_url != meta.source_url else None,
            "short_url": None if meta.doi else meta.short_url,
            "source_url": meta.source_url,
            "md5": self.md5 or self._attachment_md5(),
            "validated": zotero.today(),
            **meta.front_matter,
        }
        ids = {k: v for k, v in ids.items() if v is not None}
        if meta.is_workbook:
            return self._workbook_stub(path, ids)
        if not path.exists():
            if meta.is_web_page and self.capture is not None:
                body = webpage.html_to_markdown(self.capture.html_path.read_text(encoding="utf-8", errors="replace"))
                frontmatter.write(path, ids, f"# {meta.title}\n\n{body}\n")
                return DONE, f"wrote {path.name} from the captured page"
            return PENDING, f"extract not found at {path}; run the extract command, then rerun ingest"
        text = path.read_text(encoding="utf-8")
        if frontmatter.split(text)[0] is None:
            raise IngestError(f"{path} has no front matter block")
        changed = frontmatter.update(
            path,
            ids,
            remove=frontmatter.LEGACY_REMOVED + (("source",) if "source_file" in ids else ()),
            rename=frontmatter.LEGACY_RENAMES,
        )
        return (DONE if changed else ALREADY), path.name

    def _attachment_md5(self) -> str | None:
        assert self.item_key
        for c in zotero.stored_attachments(self.item_key):
            if c["data"].get("md5"):
                return c["data"]["md5"]
        return None

    def _workbook_stub(self, path: Path, ids: dict[str, Any]) -> tuple[str, str]:
        meta = self.meta
        in_repo = bool(meta.workbook_in_repo) or (self._local is not None and not workbook.too_large(self._local))
        filename = path.with_suffix(".xlsx").name
        if in_repo and self._local is not None:
            workbook.copy_into_repo(self._local, path.with_suffix(".xlsx"))
        ids["repo_file"] = workbook.repo_file_field(in_repo, filename)
        if not in_repo:
            self.report.notes.append(
                "workbook is not in the repo; fetch it with `just fetch-source " + meta.citekey + "`"
            )
        elif self._local is not None and workbook.too_large(self._local):
            self.report.notes.append(f"commit the large workbook with {workbook.SKIP_HINT}")
        workbook.write_stub(path, ids, meta.title, meta.index_row or meta.title, self._local)
        return DONE, f"stub {path.name}; workbook {'in repo' if in_repo else 'Zotero only'}"

    def index_rows(self) -> tuple[str, str]:
        meta, path = self.meta, self.extract_path
        if path is None or not path.exists() or not meta.index_row:
            return SKIPPED, "no extract or index_row"
        sources = self.repo_root / "context" / "sources"
        rel = path.resolve().relative_to(sources.resolve()).as_posix()
        readme = self.repo_root / "context" / "README.md"
        out = [f"global: {indexes.upsert_global_row(rel, meta.index_row, readme)}"]
        folder_readme = path.parent / "README.md"
        if meta.folder_row is not None and folder_readme.exists():
            out.append(f"folder: {indexes.upsert_folder_row(folder_readme, path.name, meta.folder_row)}")
        return DONE, "; ".join(out)

    # --- driver ---------------------------------------------------------------------------------------

    def run(self) -> IngestReport:
        """Everything up to (not including) publishing short links and tagging ``processed``."""
        report = self.report
        if not self._step("validate", self.validate):
            return report
        if not self._step("projects", self.new_projects):
            return report
        self._step("file", self.resolve_file)
        if not self._step("zotero_item", self.ensure_item):
            return report
        report.item_key = self.item_key
        assert self.item_key
        item = zotero.get_item(self.item_key)
        report.zotero_web, report.zotero_desktop = zotero.web_link(item), zotero.desktop_link(self.item_key)
        if self.meta.is_web_page and not self._step("capture", self.capture_page):
            return report
        started = self._step(
            "documentcloud_start", self.documentcloud_start
        )  # Zotero uploads while DocumentCloud processes
        self._step("zotero_files", self.attach_original)
        if started:
            self._step("documentcloud", self.documentcloud_ready)
        self._step("drive", self.drive)
        self._step("wayback", self.wayback)
        self._step("short_link", self.short_link)
        self._step("front_matter", self.front_matter)
        self._step("index", self.index_rows)
        report.public_url = self.meta.public_url
        report.short_url = None if self.meta.doi else self.meta.short_url
        return report

    def verify(self) -> list[str]:
        """Everything that must be true before the item is tagged ``processed``; empty list when it is."""
        meta = self.meta
        assert self.item_key
        problems: list[str] = []
        data = zotero.get_item(self.item_key)["data"]
        if extra.get(data.get("extra"), extra.CITATION_KEY) != meta.citekey:
            problems.append("Zotero Extra does not pin the citation key")
        if data.get("url") != meta.citation_url:
            problems.append(f"Zotero url is {data.get('url')!r}, expected {meta.citation_url!r}")
        cols = zotero.project_collections()
        have = set(data.get("collections") or [])
        for p in meta.projects:
            if cols.get(p) not in have:
                problems.append(f"not in project collection {p}")
        inbox = zotero.inbox_key()
        if inbox and inbox in have:
            problems.append("still in the Inbox")
        stored = zotero.stored_attachments(self.item_key)
        if (self.source or self.capture) and not stored:
            problems.append("no stored file attached")
        if self.md5 and stored and self.md5 not in {c["data"].get("md5") for c in stored}:
            problems.append("attached file md5 differs from the local file")
        if meta.short_link_target and self.links is not None and self.links.get(meta.citekey) != meta.short_link_target:
            problems.append("short link is not in links.json")
        return problems

    def finalize(self) -> IngestReport:
        """Verify, then tag ``processed``. Call after short links are published (so the tag means "done")."""
        report = self.report
        if report.item_key is None or report.failed:
            return report
        for step in report.steps:
            if step.name == "short_link" and step.status == PENDING:
                step.status = DONE
        if report.pending:
            report.notes.append("not marked processed: " + ", ".join(s.name for s in report.pending))
            return report
        problems = self.verify()
        if problems:
            report.add("verify", FAILED, "; ".join(problems))
            return report
        zotero.mark_processed(report.item_key)
        report.add("processed", DONE, "tagged processed")
        report.processed = True
        return report


def ingest(
    meta: metadata.SourceMetadata,
    source: Path | None = None,
    zotero_item: str | None = None,
    extract: Path | None = None,
    force: bool = False,
    publish: bool = True,
    repo_root: Path | None = None,
) -> IngestReport:
    """Ingest one document with its own short-link commit (use :func:`ingest_batch` for many)."""
    return ingest_batch([(meta, source, zotero_item, extract)], force=force, publish=publish, repo_root=repo_root)[0]


def ingest_batch(
    entries: list[tuple[metadata.SourceMetadata, Path | None, str | None, Path | None]],
    force: bool = False,
    publish: bool = True,
    repo_root: Path | None = None,
    links: shortlinks.Batch | None = None,
) -> list[IngestReport]:
    """Ingest documents one after another; publish all short links in one commit; then verify and tag each.

    One document failing does not stop the others. With ``publish=False`` short links stay queued locally and
    nothing is tagged processed.
    """
    batch = links or shortlinks.Batch()
    runs = [Ingest(m, s, z, e, links=batch, force=force, repo_root=repo_root) for m, s, z, e in entries]
    for run in runs:
        save_card(run.meta)
        try:
            run.run()
        except Exception as e:
            run.report.add("unexpected", FAILED, f"{type(e).__name__}: {e}")
    published = False
    if publish and any(r.report.item_key for r in runs):
        try:
            batch.publish()
            published = True
        except Exception as e:
            for run in runs:
                run.report.add("short_links_publish", FAILED, f"{type(e).__name__}: {e}")
    for run in runs:
        if publish and (published or not any(s.status == PENDING and s.name == "short_link" for s in run.report.steps)):
            try:
                run.finalize()
            except Exception as e:
                run.report.add("finalize", FAILED, f"{type(e).__name__}: {e}")
        elif not publish:
            run.report.notes.append("short links not published (--no-publish); item not tagged processed")
    return [r.report for r in runs]
