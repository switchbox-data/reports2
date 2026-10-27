"""Find citation keys in Quarto/Markdown sources, following pandoc's citation syntax.

Covers ``@key`` in every form (``[see @key, p. 4]``, ``[@a; @key]``, ``[-@key]``, narrative
``@key``), braced ``@{key}``, and ``#ref-key`` links. Fenced code blocks and inline code are
skipped, as are email addresses and Quarto cross-references (``@fig-...``).
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

CROSSREF_PREFIXES = (
    "fig-",
    "tbl-",
    "sec-",
    "eq-",
    "lst-",
    "thm-",
    "lem-",
    "cor-",
    "prp-",
    "cnj-",
    "def-",
    "exm-",
    "exr-",
)
EXCLUDED_DIRS = frozenset({"docs", "_freeze", ".diff", "cache", ".quarto", "node_modules"})

# pandoc: a key starts with a letter, digit or "_"; internal punctuation is allowed only
# when followed by a letter, digit or "_", so trailing punctuation is not part of the key.
_KEY = r"[A-Za-z0-9_](?:[A-Za-z0-9_]|[:.#$%&\-+?<>~/](?=[A-Za-z0-9_]))*"
CITATION_RE = re.compile(rf"(?<![A-Za-z0-9_.@])-?@(?:\{{(?P<braced>[^}}\s]+)\}}|(?P<key>{_KEY}))")
REF_LINK_RE = re.compile(rf"\(#ref-(?P<key>{_KEY})\)")
_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
_INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")


@dataclass(frozen=True)
class Citation:
    path: Path
    line: int
    key: str


def _prose_lines(text: str) -> Iterator[tuple[int, str]]:
    """Lines outside fenced code, with inline code blanked out (offsets preserved)."""
    fence: str | None = None
    for n, line in enumerate(text.splitlines(), start=1):
        if m := _FENCE_RE.match(line):
            marker = m.group(2)
            if fence is None:
                fence = marker[0] * len(marker)
                continue
            if marker.startswith(fence):
                fence = None
                continue
        if fence is None:
            yield n, _INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def find_citations(text: str, path: Path = Path("-")) -> list[Citation]:
    """Every citation key in ``text`` (Quarto cross-references excluded).

    >>> [c.key for c in find_citations("See [@madpu_Docket23150Order_2024, p. 4] and -@a_B_2020; email x@y.org.")]
    ['madpu_Docket23150Order_2024', 'a_B_2020']
    """
    found = []
    for n, line in _prose_lines(text):
        for m in CITATION_RE.finditer(line):
            key = m.group("braced") or m.group("key")
            if not key.startswith(CROSSREF_PREFIXES):
                found.append(Citation(path, n, key))
        found.extend(Citation(path, n, m.group("key")) for m in REF_LINK_RE.finditer(line))
    return found


def report_sources(reports_dir: Path) -> list[Path]:
    """``.qmd`` and ``.md`` files under ``reports/``, excluding rendered output and caches."""
    return sorted(
        p
        for p in reports_dir.rglob("*")
        if p.suffix in (".qmd", ".md") and p.is_file() and not EXCLUDED_DIRS & set(p.relative_to(reports_dir).parts)
    )
