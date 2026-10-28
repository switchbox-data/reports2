"""The approved details card for one source, and its validation against the conventions.

The agent drafts a card (see ``.cursor/skills/ingest-source``), the person approves it, and the card is
saved as YAML for ``just sources-ingest``. Validation enforces what ``context/code/source_metadata_conventions.md``
says in code: the citation key is the rule's key (or a free suffix of it), abbreviations sit on organization
authors, proceeding documents are titled ``Docket <number>: <title>``, titles are not in capitals, publishers do
not repeat the author, and project names are snake_case.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from lib.sources import checks, citekeys, docket_titles, extra, title_case

SHORT_LINK_BASE = "https://pub.switch.box"
PROJECT_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")

# Where each Zotero item type keeps the publisher (or institution), and the name of its container
# (journal, website, blog), for the types sources are filed under.
PUBLISHER_FIELD = {
    "document": "publisher",
    "report": "institution",
    "dataset": "repository",
    "webpage": "publisher",
    "journalArticle": "publisher",
    "blogPost": "publisher",
    "presentation": "meetingName",
    "book": "publisher",
    "thesis": "university",
    "preprint": "repository",
    "conferencePaper": "publisher",
    "magazineArticle": "publisher",
    "newspaperArticle": "publisher",
    "hearing": "publisher",
}
CONTAINER_FIELD = {
    "webpage": "websiteTitle",
    "journalArticle": "publicationTitle",
    "blogPost": "blogTitle",
    "magazineArticle": "publicationTitle",
    "newspaperArticle": "publicationTitle",
    "conferencePaper": "proceedingsTitle",
}
ITEM_TYPES = tuple(PUBLISHER_FIELD)
# Types that can carry a file in addition to the record itself.
WORKBOOK_TYPES = ("dataset", "document", "report")

ItemType = Literal[
    "document",
    "report",
    "dataset",
    "webpage",
    "journalArticle",
    "blogPost",
    "presentation",
    "book",
    "thesis",
    "preprint",
    "conferencePaper",
    "magazineArticle",
    "newspaperArticle",
    "hearing",
]


class MetadataError(ValueError):
    """The card breaks one or more conventions; ``problems`` lists them."""

    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = problems


class Creator(BaseModel):
    """An organization (``name``) or a person (``first_name`` and ``last_name``)."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    creator_type: str = "author"

    @model_validator(mode="after")
    def _one_form(self) -> Creator:
        person = bool(self.first_name or self.last_name)
        if self.name and person:
            raise ValueError("a creator is either an organization (name) or a person (first_name, last_name)")
        if not self.name and not (self.first_name and self.last_name):
            raise ValueError("a creator needs a name, or both first_name and last_name")
        return self

    @property
    def is_organization(self) -> bool:
        return self.name is not None

    def zotero(self) -> dict[str, str]:
        if self.name:
            return {"creatorType": self.creator_type, "name": self.name}
        return {"creatorType": self.creator_type, "firstName": self.first_name or "", "lastName": self.last_name or ""}


class SourceMetadata(BaseModel):
    """The approved card for one document (PDF, workbook or web page)."""

    model_config = ConfigDict(extra="forbid")

    citekey: str
    item_type: ItemType
    title: str
    creators: list[Creator] = Field(min_length=1)
    abbreviation: str | None = None
    new_organization: bool = False
    abbreviation_source: str | None = None
    date: str | None = None
    publisher: str | None = None
    container: str | None = None
    docket: str | None = None
    projects: list[str] = Field(default_factory=list)
    new_project: bool = False
    extract_path: str | None = None  # repo-relative; the extract's (or workbook stub's) path
    source_file: str | None = None  # the original file's name
    source_url: str | None = None
    upload_documentcloud: bool | None = None
    doi: str | None = None
    doi_source: str | None = None
    workbook_in_repo: bool | None = None
    index_row: str | None = None  # one sentence for the global index
    folder_row: list[str] | None = None  # cells after the file column in the folder README's table
    front_matter: dict[str, Any] = Field(default_factory=dict)  # descriptive fields for the extract
    access_date: str | None = None  # web pages
    # Filled in by ingest as the public copies come into existence; not part of the approved card.
    documentcloud_url: str | None = None
    drive_url: str | None = None
    wayback_url: str | None = None

    # --- derived -------------------------------------------------------------------------------

    @property
    def is_web_page(self) -> bool:
        return self.item_type == "webpage"

    @property
    def should_upload_documentcloud(self) -> bool:
        """Default: upload PDFs unless the source has a DOI or is a web page; the card can override.

        Workbooks never go to DocumentCloud (they are hosted on Google Drive).
        """
        if self.is_workbook:
            return False
        if self.upload_documentcloud is not None:
            return self.upload_documentcloud
        return not (self.doi or self.is_web_page)

    @property
    def public_url(self) -> str | None:
        """The copy readers reach: DocumentCloud, Drive, a web page's Wayback snapshot, or doi.org.

        A web page whose site blocks the Wayback Machine falls back to the live page.
        """
        if self.documentcloud_url:
            return self.documentcloud_url
        if self.drive_url:
            return self.drive_url
        if self.is_web_page and (self.wayback_url or self.source_url):
            return self.wayback_url or self.source_url
        if self.doi:
            return f"https://doi.org/{self.doi}"
        return self.source_url

    @property
    def citation_url(self) -> str:
        """What the Zotero ``url`` field (and so the citation) holds: the DOI link, else the short link."""
        if self.doi:
            return f"https://doi.org/{self.doi}"
        return f"{SHORT_LINK_BASE}/{self.citekey}"

    @property
    def short_url(self) -> str:
        return f"{SHORT_LINK_BASE}/{self.citekey}"

    @property
    def short_link_target(self) -> str | None:
        """Where the short link forwards; ``None`` for DOI items (they link to doi.org directly)."""
        return None if self.doi else self.public_url

    @property
    def is_workbook(self) -> bool:
        return bool(self.source_file and self.source_file.lower().endswith((".xlsx", ".xlsm", ".xls")))

    # --- Zotero shape --------------------------------------------------------------------------

    def extra_text(self) -> str:
        text = extra.set_field("", extra.CITATION_KEY, self.citekey)
        if self.abbreviation:
            text = extra.set_field(text, extra.SHORTAUTHOR, self.abbreviation)
        return extra.set_field(text, extra.DOCKET, self.docket) if self.docket else text

    def zotero_data(self, collection_keys: list[str] | None = None) -> dict[str, Any]:
        """The item as Zotero JSON (key and version omitted), ready to create."""
        data: dict[str, Any] = {
            "itemType": self.item_type,
            "title": self.title,
            "creators": [c.zotero() for c in self.creators],
            "extra": self.extra_text(),
            "url": self.citation_url,
            "tags": [],
            "collections": list(collection_keys or []),
            "relations": {},
        }
        if self.date:
            data["date"] = self.date
        if self.doi:
            data["DOI"] = self.doi
        if self.publisher:
            data[PUBLISHER_FIELD[self.item_type]] = self.publisher
        if self.container and (field := CONTAINER_FIELD.get(self.item_type)):
            data[field] = self.container
        if self.access_date:
            data["accessDate"] = self.access_date
        return data

    # --- validation ----------------------------------------------------------------------------

    def problems(self, taken: set[str] | None = None) -> list[str]:
        """Everything on the card that breaks a convention (empty when it is fine).

        ``taken`` holds the pinned keys of every other item in the library.
        """
        out: list[str] = []
        data = self.zotero_data()
        # Key: the rule's key, or the rule's key with a free collision suffix.
        try:
            base = citekeys.base_key(data)
        except citekeys.NoCreatorError as e:
            return [str(e)]
        m = re.fullmatch(re.escape(base) + r"([a-z]{0,2})", self.citekey)
        if not m:
            out.append(f"citekey {self.citekey!r} is not the rule's key {base!r} (or that key with a suffix a, b, ...)")
        elif taken is not None and self.citekey in taken:
            free = citekeys.propose_key(data, taken)
            out.append(f"citekey {self.citekey!r} is already used by another item; the next free key is {free!r}")
        if self.citekey and checks.key_not_citable(self.citekey):
            out.append(f"citekey {self.citekey!r} would be read as Markdown emphasis; it cannot be cited")
        if self.abbreviation and not self.creators[0].is_organization:
            out.append("an abbreviation belongs on an organization author; the first author is a person")
        if self.abbreviation and self.new_organization and not self.abbreviation_source:
            out.append("a new organization's abbreviation needs abbreviation_source (where the short form comes from)")
        if self.abbreviation and self.abbreviation.strip().upper() in {"DPU", "PSC", "PUC", "DEC", "DPS"}:
            out.append(f"bare {self.abbreviation!r} is never valid; add the state prefix (MA DPU, NY PSC, ...)")
        if self.title_all_caps():
            out.append(f"title is in ALL CAPS; use {title_case.uncap_title(self.title)!r}")
        suggestion = docket_titles.docket_title(self.title)
        if suggestion:
            out.append(f"title should read {suggestion!r} (Docket <number>: <title>)")
        if self.docket and not self.title.startswith(f"Docket {self.docket}: "):
            out.append(f"a card with docket {self.docket!r} needs the title 'Docket {self.docket}: <title>'")
        if self.publisher and self.repeats_author(self.publisher):
            out.append("publisher repeats the author; leave it out unless it names a different organization")
        for p in self.projects:
            if not PROJECT_RE.match(p):
                out.append(f"project {p!r} must be lowercase snake_case")
        if not self.projects:
            out.append("every source belongs to a project (use general_reference for sources that serve no report)")
        if self.new_project and not self.projects:
            out.append("new_project is set but no project is named")
        if self.date and not DATE_RE.match(self.date):
            out.append(f"date {self.date!r} must be YYYY, YYYY-MM or YYYY-MM-DD")
        if self.doi and not DOI_RE.match(self.doi):
            out.append(f"doi {self.doi!r} must look like 10.xxxx/suffix (no URL prefix)")
        if self.is_workbook and self.item_type not in WORKBOOK_TYPES:
            out.append(f"a workbook is filed as dataset, document or report, not {self.item_type!r}")
        if self.is_workbook and self.upload_documentcloud:
            out.append("DocumentCloud cannot host workbooks; they go to Google Drive")
        if self.is_web_page and not self.source_url:
            out.append("a web page needs source_url")
        return out

    def check(self, taken: set[str] | None = None) -> None:
        """Raise :class:`MetadataError` listing every problem."""
        if problems := self.problems(taken):
            raise MetadataError(problems)

    def title_all_caps(self) -> bool:
        return title_case.is_all_caps(self.title)

    def repeats_author(self, publisher: str) -> bool:
        norm = _squash(publisher)
        names = [c.name for c in self.creators if c.name]
        return norm in {_squash(n) for n in names} or (
            bool(self.abbreviation) and norm == _squash(self.abbreviation or "")
        )


def _squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.casefold())


def load(path: Path) -> SourceMetadata:
    """Read an approved card from YAML."""
    return SourceMetadata.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")))


def dump(meta: SourceMetadata, path: Path) -> None:
    """Write a card as YAML (without the fields ingest fills in)."""
    body = meta.model_dump(exclude_none=True, exclude={"documentcloud_url", "drive_url", "wayback_url"})
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(yaml.safe_dump(body, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
