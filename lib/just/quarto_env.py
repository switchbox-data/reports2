"""Quarto subprocess environment for ``just render`` / ``draft`` / ``typeset``."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _venv_python(root: Path) -> Path | None:
    """Return ``<root>/.venv/bin/python*`` if that venv exists."""
    bindir = root / ".venv" / "bin"
    if not (root / ".venv" / "pyvenv.cfg").is_file():
        return None
    for name in ("python3", "python"):
        candidate = bindir / name
        if candidate.is_file():
            # Keep the venv shim path; resolving symlinks to system python
            # drops site-packages and breaks Jupyter/nbformat discovery.
            return candidate.absolute()
    return None


def _repo_root_from_cwd() -> Path | None:
    """Walk up from ``cwd`` for a directory that looks like reports2."""
    for root in (Path.cwd(), *Path.cwd().parents):
        if (root / "pyproject.toml").is_file() and _venv_python(root) is not None:
            return root
    return None


def resolve_quarto_python() -> str | None:
    """Return the Python interpreter Quarto should use, if we can infer one.

    On shared EC2 hosts each user keeps their own checkout
    (``/ebs/home/<user>/reports2/.venv``). Discovery is relative to the
    running interpreter or the current working directory's ancestor tree.

    When a project venv is found we always prefer it over any inherited
    ``QUARTO_PYTHON`` — a stale shell export to system ``python3`` is a
    common cause of missing-``nbformat`` render failures on this box.
    """
    exe = Path(sys.executable)
    if (exe.parent.parent / "pyvenv.cfg").is_file():
        return str(exe.absolute())

    repo_root = _repo_root_from_cwd()
    if repo_root is not None:
        venv_python = _venv_python(repo_root)
        if venv_python is not None:
            return str(venv_python)

    return None


def quarto_env(**overrides: str) -> dict[str, str]:
    """Build an environment dict for ``subprocess.run([...quarto...])``."""
    env = os.environ.copy()
    python = resolve_quarto_python()
    if python is not None:
        env["QUARTO_PYTHON"] = python
        env["VIRTUAL_ENV"] = str(Path(python).parent.parent)
    env.update(overrides)
    return env
