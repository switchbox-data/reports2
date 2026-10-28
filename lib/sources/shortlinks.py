"""Short links ``https://pub.switch.box/<citation-key>``, served from the ``switchbox-data/pub`` GitHub Pages repo.

``links.json`` (citation key -> destination) is the source of truth. ``404.html`` is generated from it and
embeds the whole map, so any key forwards with a single request and no per-link page. Work happens on a local
clone under ``SOURCES_CACHE_DIR/pub``; a batch of changes is one commit and one push. These pushes are the
pipeline's only automatic commits, and they go to ``pub``, never to reports2.

``switchbox-data/pub`` and the ``switch.box`` domain registration are critical infrastructure: every printed
citation depends on them.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from lib.sources import env

DEFAULT_REMOTE = "https://github.com/switchbox-data/pub.git"
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")

_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Switchbox source</title>
<meta name="robots" content="noindex">
<script>
  var LINKS = __LINKS__;
  var key = "";
  try { key = decodeURIComponent(location.pathname.replace(/^\\/+|\\/+$/g, "")); } catch (e) {}
  var target = Object.prototype.hasOwnProperty.call(LINKS, key) ? LINKS[key] : null;
  if (target && /^https?:\\/\\//i.test(target)) { location.replace(target); }
</script>
<style>body{font-family:system-ui,sans-serif;max-width:36rem;margin:4rem auto;padding:0 1rem;color:#023047}</style>
</head>
<body>
<noscript><p>This short link needs JavaScript to forward you. See <a href="links.json">the list of links</a>.</p></noscript>
<p id="msg"></p>
<script>
  var msg = document.getElementById("msg");
  var a = document.createElement("a");
  if (target && /^https?:\\/\\//i.test(target)) {
    msg.appendChild(document.createTextNode("Forwarding to "));
    a.href = target;
    a.textContent = target;
    msg.appendChild(a);
    msg.appendChild(document.createTextNode("\\u2026"));
  } else {
    msg.appendChild(document.createTextNode("No source found at this link. Visit "));
    a.href = "https://switch.box/";
    a.textContent = "switch.box";
    msg.appendChild(a);
    msg.appendChild(document.createTextNode("."));
  }
</script>
</body>
</html>
"""


class ShortLinkError(ValueError):
    """A key or destination is not acceptable, or an existing link would be overwritten silently."""


def check_key(key: str) -> None:
    if not KEY_RE.match(key):
        raise ShortLinkError(f"short-link key {key!r} may only contain letters, digits, '_', '.' and '-'")


def check_target(target: str) -> None:
    parts = urlsplit(target)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ShortLinkError(f"short-link destination {target!r} must be an http(s) URL")


def render_404(links: dict[str, str]) -> str:
    """The generated ``404.html`` for ``links``.

    The map is embedded as JSON with every ``<`` escaped, so a destination cannot close the script tag, and the
    page builds its content with DOM calls (never ``innerHTML``) and forwards only to http(s) URLs.
    """
    blob = json.dumps(dict(sorted(links.items())), ensure_ascii=True)
    blob = blob.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return _TEMPLATE.replace("__LINKS__", blob)


def clone_dir() -> Path:
    return env.cache_dir() / "pub"


def remote_url() -> str:
    return os.environ.get("SOURCES_PUB_REMOTE", DEFAULT_REMOTE)


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def _unpushed(repo: Path) -> bool:
    """Whether the clone has commits its upstream lacks."""
    out = _git(repo, "rev-list", "--count", "@{upstream}..HEAD", check=False)
    return out.returncode == 0 and int(out.stdout.strip() or 0) > 0


def ensure_clone(path: Path | None = None) -> Path:
    """The local clone of ``pub``: cloned when absent, otherwise brought up to date (fast-forward only)."""
    repo = Path(path) if path else clone_dir()
    if not (repo / ".git").exists():
        repo.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", remote_url(), str(repo)], capture_output=True, text=True, check=True)
    else:
        _git(repo, "pull", "--ff-only")
    return repo


def load_links(repo: Path) -> dict[str, str]:
    path = repo / "links.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_links(repo: Path, links: dict[str, str]) -> bool:
    """Write ``links.json`` (sorted, 2-space indent) and ``404.html``; True when either file changed."""
    texts = {
        "links.json": json.dumps(dict(sorted(links.items())), indent=2, ensure_ascii=False) + "\n",
        "404.html": render_404(links),
    }
    changed = False
    for name, text in texts.items():
        path = repo / name
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            changed = True
    return changed


def regenerate(repo: Path) -> bool:
    """Rebuild ``404.html`` from ``links.json``; True when it changed."""
    links = load_links(repo)
    page = repo / "404.html"
    text = render_404(links)
    if page.exists() and page.read_text(encoding="utf-8") == text:
        return False
    page.write_text(text, encoding="utf-8")
    return True


@dataclass
class Batch:
    """A set of short-link changes published as one commit and one push.

    ``add`` is a no-op for an unchanged link and refuses to overwrite a different destination (use ``repoint``).
    """

    repo: Path | None = None
    message: str | None = None
    ops: list[tuple[str, str, str]] = field(default_factory=list)  # ("add"|"repoint", key, target)

    def __post_init__(self) -> None:
        self.repo = ensure_clone(self.repo)
        self._links = load_links(self.repo)

    def add(self, key: str, target: str) -> bool:
        check_key(key)
        check_target(target)
        if key in self._links:
            if self._links[key] == target:
                return False
            raise ShortLinkError(f"{key} already points to {self._links[key]}; use repoint to change it")
        self._links[key] = target
        self.ops.append(("add", key, target))
        return True

    def repoint(self, key: str, target: str) -> bool:
        check_key(key)
        check_target(target)
        if self._links.get(key) == target:
            return False
        self._links[key] = target
        self.ops.append(("repoint", key, target))
        return True

    def get(self, key: str) -> str | None:
        return self._links.get(key)

    def publish(self) -> bool:
        """Write both files, commit and push once. Returns False when there was nothing to commit or push.

        Commits left unpushed by an earlier failed run are pushed too, so a rerun finishes the job.
        """
        repo = self.repo
        assert repo is not None
        changed = save_links(repo, self._links)
        if changed:
            _git(repo, "add", "links.json", "404.html")
            _git(repo, "commit", "-m", self.message or self._default_message())
        elif not _unpushed(repo):
            return False
        pushed = _git(repo, "push", check=False)
        if pushed.returncode != 0:
            # Someone else pushed first: start from their state, replay this batch, push again.
            _git(repo, "fetch", "origin")
            _git(repo, "reset", "--hard", "@{upstream}")
            links = load_links(repo)
            for _, key, target in self.ops:
                links[key] = target
            self._links = links
            if save_links(repo, links):
                _git(repo, "add", "links.json", "404.html")
                _git(repo, "commit", "-m", self.message or self._default_message())
            _git(repo, "push")
        return True

    def _default_message(self) -> str:
        added = [k for op, k, _ in self.ops if op == "add"]
        moved = [k for op, k, _ in self.ops if op == "repoint"]
        parts = []
        if added:
            parts.append(f"Add {len(added)} short link{'s' if len(added) != 1 else ''}")
        if moved:
            parts.append(f"repoint {len(moved)}")
        detail = ", ".join((added + moved)[:3]) + (" ..." if len(added + moved) > 3 else "")
        return f"{' and '.join(parts) or 'Regenerate 404.html'}: {detail}".rstrip(": ")


def resolve(key: str, repo: Path | None = None) -> str | None:
    """Where ``key`` forwards according to the local clone (after a pull); ``None`` when unknown."""
    return load_links(ensure_clone(repo)).get(key)
