"""Tests for lib.just.quarto_env."""

from __future__ import annotations

from pathlib import Path

from lib.just.quarto_env import quarto_env, resolve_quarto_python


def test_quarto_env_uses_running_interpreter_without_resolving_symlink(monkeypatch) -> None:
    monkeypatch.delenv("QUARTO_PYTHON", raising=False)
    fake_python = Path("/ebs/home/alice/reports2/.venv/bin/python3")
    monkeypatch.setattr("lib.just.quarto_env.sys.executable", str(fake_python))

    def fake_is_file(self: Path) -> bool:
        if self == fake_python:
            return True
        return self.name == "pyvenv.cfg" and self.parent.name == ".venv"

    monkeypatch.setattr("lib.just.quarto_env.Path.is_file", fake_is_file)

    assert resolve_quarto_python() == str(fake_python.absolute())
    assert quarto_env()["QUARTO_PYTHON"] == str(fake_python.absolute())


def test_quarto_env_finds_repo_venv_from_cwd(monkeypatch) -> None:
    monkeypatch.delenv("QUARTO_PYTHON", raising=False)
    repo = Path("/ebs/home/bob/reports2")
    venv_python = repo / ".venv" / "bin" / "python3"
    report_dir = repo / "reports" / "md_hp_rates"
    monkeypatch.setattr("lib.just.quarto_env.sys.executable", "/usr/bin/python3")
    monkeypatch.setattr("lib.just.quarto_env.Path.cwd", lambda: report_dir)

    def fake_is_file(self: Path) -> bool:
        if self == repo / "pyproject.toml":
            return True
        if self == repo / ".venv" / "pyvenv.cfg":
            return True
        return self == venv_python

    monkeypatch.setattr("lib.just.quarto_env.Path.is_file", fake_is_file)

    assert resolve_quarto_python() == str(venv_python.absolute())


def test_quarto_env_respects_existing_quarto_python_when_no_venv(monkeypatch) -> None:
    monkeypatch.setenv("QUARTO_PYTHON", "/opt/venv/bin/python")
    monkeypatch.setattr("lib.just.quarto_env.sys.executable", "/usr/bin/python3")

    def fake_is_file(self: Path) -> bool:
        return False

    monkeypatch.setattr("lib.just.quarto_env.Path.is_file", fake_is_file)

    assert resolve_quarto_python() is None
    assert quarto_env()["QUARTO_PYTHON"] == "/opt/venv/bin/python"


def test_quarto_env_overrides_stale_shell_quarto_python(monkeypatch) -> None:
    monkeypatch.setenv("QUARTO_PYTHON", "/usr/bin/python3.13")
    fake_python = Path("/ebs/home/alice/reports2/.venv/bin/python3")
    monkeypatch.setattr("lib.just.quarto_env.sys.executable", str(fake_python))

    def fake_is_file(self: Path) -> bool:
        if self == fake_python:
            return True
        return self.name == "pyvenv.cfg" and self.parent.name == ".venv"

    monkeypatch.setattr("lib.just.quarto_env.Path.is_file", fake_is_file)

    env = quarto_env()
    assert env["QUARTO_PYTHON"] == str(fake_python.absolute())
    assert env["VIRTUAL_ENV"] == str(fake_python.parent.parent.absolute())


def test_quarto_env_merges_overrides(monkeypatch) -> None:
    monkeypatch.delenv("QUARTO_PYTHON", raising=False)
    env = quarto_env(SWITCHBOX_GT_AS_IMAGE="1")
    assert env["SWITCHBOX_GT_AS_IMAGE"] == "1"
