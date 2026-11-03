"""Find the notebook cell that produces a report variable or figure, at the provenance tag."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from lib.provenance.config import Link, ProvenanceConfig, Resolver


def git_show(rev: str, path: str, repo: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "show", f"{rev}:{path}"], check=True, capture_output=True, text=True
    ).stdout


@dataclass
class Notebook:
    name: str
    lines: list[str]
    cells: list[tuple[int, int]]


def load_notebook(cfg: ProvenanceConfig, name: str) -> Notebook:
    lines = git_show(cfg.tag, f"{cfg.report_rel}/{cfg.notebook_path(name)}", cfg.path_repo).splitlines()
    cells: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("```{"):
            start = i
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            cells.append((start + 1, i + 1))
        i += 1
    return Notebook(name, lines, cells)


def cell_for_line(nb: Notebook, line: int) -> tuple[int, int]:
    for s, e in nb.cells:
        if s <= line <= e:
            return s, e
    return line, line


def _template_regex(template: str) -> tuple[re.Pattern[str], int]:
    parts = re.split(r"\{[^}]*\}", template)
    literal = sum(len(p) for p in parts)
    return re.compile("[A-Za-z0-9_]+".join(re.escape(p) for p in parts)), literal


def find_var_line(nb: Notebook, var: str) -> int | None:
    literal_re = re.compile(
        r"""(?:\w+_vars\[\s*["']"""
        + re.escape(var)
        + r"""["']\s*\]\s*=(?!=))|(?:^\s*["']"""
        + re.escape(var)
        + r"""["']\s*:)"""
    )
    hits = [k + 1 for k, ln in enumerate(nb.lines) if literal_re.search(ln)]
    if hits:
        return hits[-1]
    best: tuple[int, int] | None = None
    tmpl_re = re.compile(r"""\w+_vars\[\s*f["']([^"']+)["']\s*\]\s*=(?!=)""")
    for k, ln in enumerate(nb.lines):
        for m in tmpl_re.finditer(ln):
            rx, literal = _template_regex(m.group(1))
            if rx.fullmatch(var) and (best is None or literal >= best[0]):
                best = (literal, k + 1)
    return best[1] if best else None


def find_label_line(nb: Notebook, label: str) -> int | None:
    rx = re.compile(r"^#\|\s*label:\s*" + re.escape(label) + r"\s*$")
    return next((k + 1 for k, ln in enumerate(nb.lines) if rx.match(ln)), None)


def fig_caption(nb: Notebook, label_line: int) -> str:
    s, e = cell_for_line(nb, label_line)
    for ln in nb.lines[s - 1 : e]:
        if m := re.match(r'^#\|\s*fig-cap:\s*"?(.*?)"?\s*$', ln):
            return m.group(1)
    return ""


def var_regex(cfg: ProvenanceConfig) -> re.Pattern[str]:
    return re.compile(r"\b(" + "|".join(list(cfg.namespaces)) + r")\.(\w+)")


@dataclass
class Resolution:
    link: Link | None
    why: str = ""
    other_cells: tuple[str, ...] = ()
    """Cells of further variables in the expression that live outside the linked cell."""


def resolve_expr(cfg: ProvenanceConfig, code: str, notebooks: dict[str, Notebook], testimony: Notebook) -> Resolution:
    found = var_regex(cfg).findall(code)
    for prefix, var in found:
        nb = notebooks[cfg.namespaces[prefix]]
        line = find_var_line(nb, var)
        if line is None:
            return Resolution(None, f"no assignment of {var!r} in {nb.name}.qmd")
        s, e = cell_for_line(nb, line)
        others: list[str] = []
        for p2, v2 in found:
            nb2 = notebooks[cfg.namespaces[p2]]
            line2 = find_var_line(nb2, v2)
            if line2 is None:
                others.append(f"{v2} (not found in {nb2.name}.qmd)")
                continue
            cell2 = cell_for_line(nb2, line2)
            if (nb2.name, cell2) != (nb.name, (s, e)):
                others.append(f"{v2} at {nb2.name}.qmd_{cell2[0]}-{cell2[1]}")
        return Resolution(cfg.notebook_link(nb.name, s, e), "", tuple(dict.fromkeys(others)))
    for resolver in cfg.resolvers:
        link = resolver(code, testimony, cfg)
        if link is not None:
            return Resolution(link)
    return Resolution(None, "no report variable or constant in expression")


def filed_constant_resolver(prefix: str = "FILED_") -> Resolver:
    """Link expressions using constants defined in the testimony setup cell (e.g. ``FILED_TX``)."""

    def resolve(code: str, testimony: Notebook, cfg: ProvenanceConfig) -> Link | None:
        consts = re.findall(rf"\b({re.escape(prefix)}[A-Z_]+)\b", code)
        lines = [k + 1 for k, ln in enumerate(testimony.lines) for c in consts if re.match(rf"^{c}\s*=", ln)]
        if lines:
            return cfg.notebook_link(testimony.name, min(lines), max(lines))
        return None

    return resolve
