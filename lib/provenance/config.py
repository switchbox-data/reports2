"""Per-testimony settings for a provenance document.

Each testimony gets a thin ``build_provenance.py`` that fills in a ``ProvenanceConfig`` and
calls ``lib.provenance.build.main``. Everything that varies between testimonies lives here:
which tag to link to, which notebooks the testimony reads, the wording at the top of the
document, and optional hooks for the parts that don't follow a template.
"""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from lib.provenance.review import Review

if TYPE_CHECKING:
    from lib.provenance.resolve import Notebook

GITHUB_REPORTS2_BLOB = "https://github.com/switchbox-data/reports2/blob"
GITHUB_RDP_BLOB = "https://github.com/switchbox-data/rate-design-platform/blob"
GITHUB_RDP_TREE = "https://github.com/switchbox-data/rate-design-platform/tree"

DEFAULT_PLATFORM_INTRO = (
    "The notebooks read results from Switchbox's rate simulation platform, which models each home's "
    "hourly electricity use, its bills under each rate, and the cost of serving it:"
)


@dataclass(frozen=True)
class Link:
    text: str
    url: str
    notebook: str = ""
    """reports2 notebook the link points into, if any (lists it under "Where the work happens")."""


@dataclass(frozen=True)
class Hardcoded:
    """A number typed into the testimony prose rather than computed inline.

    ``context`` is a run of words around the number as printed in the PDF (it must contain
    ``value``); it pins down which occurrence is meant.
    """

    value: str
    context: str
    link: Link
    review_note: str = ""
    """Anything a reviewer should know about this number (written to the review CSV only)."""


@dataclass(frozen=True)
class KnownDifference:
    """A filed number that differs from the code's rendered value for a reason already explained."""

    pdf_value: str
    cache_value: str
    explanation: str


Resolver = Callable[[str, "Notebook", "ProvenanceConfig"], Link | None]
RunChecks = Callable[[Review], None]


@dataclass
class ProvenanceConfig:
    tag: str
    """Git ref (normally an annotated tag) that every reports2 permalink points to."""
    path_repo: Path
    """reports2 checkout used to read files at ``tag``."""
    report_rel: str
    """Report directory relative to the repo root, e.g. ``reports/md_hp_rates``."""
    path_pdf: Path
    """The testimony as filed."""
    namespaces: dict[str, str]
    """Setup-cell variable prefix -> notebook name, e.g. ``{"r": "representative_home"}``."""
    notebook_blurbs: dict[str, tuple[str, str]]
    """Notebook name -> (plain-language title, one-sentence description)."""
    title: str
    subtitle: str
    intro: str
    docx_name: str
    qmd_name: str = "expert_testimony.qmd"
    pdf_md5: str | None = None
    """md5 of the filed PDF, checked before indexing; defaults to the md5 in ``path_extract``'s front matter."""
    path_extract: Path | None = None
    """The filed PDF's validated source extract (``context/sources/...``, ``citation_scheme: page_line``);
    every number's page and line is cross-checked against it with ``lib.sources.pagelines.cite``."""
    path_exec_dir: Path | None = None
    """Directory the setup cell runs in, so its relative ``cache/`` paths resolve. Defaults to the
    report directory; point it at a worktree checked out at ``tag`` when the local cache is newer."""
    path_baseline_docx: Path | None = None
    """Optional pre-filing render, used to tell Word edits apart from cache drift."""
    platform_intro: str = DEFAULT_PLATFORM_INTRO
    platform_links: list[str] = field(default_factory=list)
    """Markdown bullets linking to rate-design-platform code and docs."""
    resolvers: list[Resolver] = field(default_factory=list)
    """Extra ways to link an inline expression when no namespace variable matches."""
    hardcoded: list[Hardcoded] = field(default_factory=list)
    known_differences: list[KnownDifference] = field(default_factory=list)
    include_namespaces: frozenset[str] | None = None
    """Only list numbers, tables and figures that use one of these prefixes (e.g. a later testimony's new
    analysis, leaving out what it repeats from an earlier one); ``None`` lists everything."""
    exclude_codes: frozenset[str] = frozenset()
    """Inline expressions to leave out even though they use an included namespace, e.g.
    ``min(d.x, s.x)`` that prints the earlier testimony's value."""
    run_checks: RunChecks | None = None

    @property
    def path_report(self) -> Path:
        return self.path_repo / self.report_rel

    @property
    def testimony_key(self) -> str:
        return Path(self.qmd_name).stem

    def includes_code(self, code: str) -> bool:
        """Whether an inline expression is listed: it uses an included namespace (as ``s.x`` or a bare
        ``f(s)``) and isn't in ``exclude_codes``."""
        if code in self.exclude_codes:
            return False
        if self.include_namespaces is None:
            return True
        names = {n.id for n in ast.walk(ast.parse(code, mode="eval")) if isinstance(n, ast.Name)}
        return bool(names & self.include_namespaces)

    def includes_notebook(self, name: str) -> bool:
        if self.include_namespaces is None:
            return True
        return any(self.namespaces.get(p) == name for p in self.include_namespaces)

    def notebook_path(self, name: str) -> str:
        """Path of a notebook relative to the report directory."""
        return self.qmd_name if name == self.testimony_key else f"notebooks/{name}.qmd"

    def notebook_link(self, name: str, start: int, end: int) -> Link:
        url = f"{GITHUB_REPORTS2_BLOB}/{self.tag}/{self.report_rel}/{self.notebook_path(name)}#L{start}-L{end}"
        return Link(f"{name}.qmd_{start}-{end}", url, name)

    def notebook_url(self, name: str) -> str:
        return f"{GITHUB_REPORTS2_BLOB}/{self.tag}/{self.report_rel}/{self.notebook_path(name)}"
