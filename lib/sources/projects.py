"""Projects: the shared name of a report folder, a Zotero subcollection and a ``context/sources/`` folder.

A source belongs to a project, and the project name is the same in all three places. ``list_projects`` is the
union of folder names in ``reports/`` (excluding ``templates``) and subcollections of Zotero's Reports
collection, plus ``context/sources/`` folders that match one of those or are clearly a planned report.
``general_reference`` (textbooks and manuals that serve no single report) is an ordinary project with a Zotero
collection and a source folder but no report folder. ``ensure_project`` creates the Zotero subcollection and the
source folder, and only when a card sets ``new_project``.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from lib.sources import env

PLANNED = frozenset({"il_hp_rates", "me_hp_rates", "nj_hp_rates", "pa_hp_rates"})


@dataclass(frozen=True)
class Project:
    """A project and where it exists today."""

    name: str
    report_folder: bool
    zotero_collection: bool
    source_folder: bool
    planned: bool = False

    @property
    def complete(self) -> bool:
        return self.zotero_collection and self.source_folder


def _dirs(path: Path, skip: Iterable[str] = ()) -> set[str]:
    if not path.is_dir():
        return set()
    return {p.name for p in path.iterdir() if p.is_dir() and not p.name.startswith((".", "_")) and p.name not in skip}


def list_projects(
    reports_dir: Path | None = None,
    sources_dir: Path | None = None,
    zotero_projects: Iterable[str] | None = None,
) -> list[Project]:
    """Projects known to the repo or Zotero, with where each exists. ``zotero_projects`` are collection names."""
    reports = _dirs(reports_dir or env.REPORTS_DIR, skip=("templates", "docs"))
    sources = _dirs(sources_dir or env.SOURCES_DIR)
    zotero = set(zotero_projects or ())
    names = reports | zotero | {n for n in sources if n in PLANNED}
    names |= {n for n in sources if n in reports or n in zotero}
    return [
        Project(
            n, n in reports, n in zotero, n in sources, planned=n in PLANNED and n not in reports and n not in zotero
        )
        for n in sorted(names)
    ]


def source_folder(name: str, sources_dir: Path | None = None) -> Path:
    """``context/sources/<name>/``."""
    return (sources_dir or env.SOURCES_DIR) / name


def ensure_project(
    name: str,
    sources_dir: Path | None = None,
    create_collection: Callable[[str], str] | None = None,
) -> dict[str, str]:
    """Create the Zotero subcollection and the source folder for a new project (both are idempotent)."""
    if create_collection is None:
        from lib.sources import zotero

        create_collection = zotero.create_project_collection
    key = create_collection(name)
    folder = source_folder(name, sources_dir)
    folder.mkdir(parents=True, exist_ok=True)
    return {"zotero_collection": key, "folder": str(folder)}
